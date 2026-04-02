const OWNER = "LotrExtendedTeam";
const REPO = "Extended-Wiki";
const BRANCH = "main"; // default upstream branch
const CLIENT_ID = "YOUR_CLIENT_ID"; // GitHub OAuth client ID

let currentPath = "";
let fileSha = "";
let accessToken = "";
let originalContent = "";

// ----------------- Logging -----------------
function log(msg, isError = false) {
  const el = document.getElementById("progressLog");
  const color = isError ? "#f66" : "#0f0";
  el.innerHTML += `<div style="color:${color}">${msg}</div>`;
  el.scrollTop = el.scrollHeight;
}

function assert(condition, msg) {
  if (!condition) throw new Error(msg);
}

// ----------------- API Wrapper -----------------
async function api(url, method = "GET", body = null) {
  const res = await fetch(url, {
    method,
    headers: {
      Authorization: `token ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : null,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${text}`);
  }

  return res.json();
}

// ----------------- Editor Modal -----------------
function openEditor(path) {
  currentPath = path;
  // If a full GitHub edit URL was passed, extract the repo-relative path
  if (path.startsWith("https://github.com/")) {
    const url = new URL(path);
    const parts = url.pathname.split("/"); // ["", "OWNER", "REPO", "edit", "main", "wiki", "docs", "index.md"]
    const editIndex = parts.indexOf("edit");
    if (editIndex !== -1 && editIndex + 2 < parts.length) {
      currentPath = parts.slice(editIndex + 2).join("/"); // "wiki/docs/index.md"
    } else {
      log("Invalid GitHub edit URL", true);
      return;
    }
  }
  document.getElementById("editorModal").style.display = "block";
  document.getElementById("diffView").style.display = "none";
  log("Loading file...");
  log(currentPath);

  (async () => {
    try {
      let ownerToUse = OWNER;
      let branchToUse = BRANCH;
      const editOwnFork = document.getElementById("editOwnFork")?.checked;

      if (accessToken && editOwnFork) {
        const user = await api("https://api.github.com/user");
        const username = user.login;

        // check if fork exists
        const forkRes = await fetch(`https://api.github.com/repos/${username}/${REPO}`);
        if (forkRes.ok) {
          ownerToUse = username;
          log("Using your fork.");
        } else {
          log("Fork not found, loading upstream instead.");
        }
      }

      const res = await fetch(
        `https://api.github.com/repos/${ownerToUse}/${REPO}/contents/${currentPath}?ref=${branchToUse}`
      );

      if (!res.ok) throw new Error(`Failed to load file (${res.status})`);

      const data = await res.json();
      fileSha = data.sha;
      originalContent = decodeURIComponent(escape(atob(data.content)));
      document.getElementById("editor").value = originalContent;

      // autofill PR title
      document.getElementById("prTitle").value = `Edit ${currentPath}`;

      log(`Loaded file from ${ownerToUse}/${REPO}`);
    } catch (err) {
      log("Error loading file: " + err.message, true);
      console.error(err);
    }
  })();
}

function extractRepoPath(editUrl) {
  try {
    // Example editUrl:
    // https://github.com/LotrExtendedTeam/Extended-Wiki/edit/main/wiki/docs/index.md
    const url = new URL(editUrl);
    const parts = url.pathname.split('/'); // ["", "LotrExtendedTeam", "Extended-Wiki", "edit", "main", "wiki", "docs", "index.md"]

    // Find index of "edit" segment
    const editIndex = parts.indexOf("edit");
    if (editIndex === -1 || editIndex + 2 >= parts.length) {
      throw new Error("Invalid GitHub edit URL");
    }

    // Repo-relative path: everything after branch
    const relativePath = parts.slice(editIndex + 2).join("/"); // ["wiki","docs","index.md"] => "wiki/docs/index.md"
    return relativePath;
  } catch (err) {
    console.error("Failed to extract repo path:", err);
    return null;
  }
}

function closeEditor() {
  document.getElementById("editorModal").style.display = "none";
}

// ----------------- GitHub OAuth -----------------
function githubLogin() {
  const redirect = encodeURIComponent(window.location.href);
  window.location.href = `https://github.com/login/oauth/authorize?client_id=${CLIENT_ID}&scope=repo&redirect_uri=${redirect}`;
}

async function handleOAuth() {
  const params = new URLSearchParams(window.location.search);
  if (params.get("code")) {
    log("Authenticating...");
    try {
      const res = await fetch(`/auth/github/exchange?code=${params.get("code")}`);
      const data = await res.json();
      accessToken = data.access_token;
      log("Logged in!");
      window.history.replaceState({}, document.title, window.location.pathname);
    } catch (err) {
      log("OAuth failed: " + err.message, true);
    }
  }
}

// ----------------- Fork Handling -----------------
async function ensureFork(username) {
  log("Checking fork...");
  let res = await fetch(`https://api.github.com/repos/${username}/${REPO}`);
  if (res.status === 404) {
    log("Fork not found. Creating...");
    await api(`https://api.github.com/repos/${OWNER}/${REPO}/forks`, "POST");
    // wait + retry
    for (let i = 0; i < 10; i++) {
      log("Waiting for fork...");
      await new Promise((r) => setTimeout(r, 2000));
      let check = await fetch(`https://api.github.com/repos/${username}/${REPO}`);
      if (check.ok) {
        log("Fork ready.");
        return;
      }
    }
    throw new Error("Fork creation timeout.");
  }
  log("Fork exists.");
}

async function getUpstreamSha() {
  const ref = await api(`https://api.github.com/repos/${OWNER}/${REPO}/git/ref/heads/${BRANCH}`);
  return ref.object.sha;
}

async function createBranch(username, branchName, baseSha) {
  log("Creating branch...");
  return api(`https://api.github.com/repos/${username}/${REPO}/git/refs`, "POST", {
    ref: `refs/heads/${branchName}`,
    sha: baseSha,
  });
}

async function commitFile(username, branchName) {
  log("Committing file...");
  const content = btoa(unescape(encodeURIComponent(document.getElementById("editor").value)));
  return api(`https://api.github.com/repos/${username}/${REPO}/contents/${currentPath}`, "PUT", {
    message: "Edit via web editor",
    content,
    sha: fileSha,
    branch: branchName,
  });
}

async function createPR(username, branchName) {
  const title = document.getElementById("prTitle").value || `Edit ${currentPath}`;
  const body = document.getElementById("prBody").value || "Submitted via web editor";
  return api(`https://api.github.com/repos/${OWNER}/${REPO}/pulls`, "POST", {
    title,
    head: `${username}:${branchName}`,
    base: BRANCH,
    body,
  });
}

// ----------------- Diff Viewer -----------------
async function ensureDiffLibrary() {
  if (typeof diff_match_patch !== "undefined") return true;
  log("Loading diff library from CDN...");
  return new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = "https://unpkg.com/diff-match-patch";
    script.onload = () => {
      log("Diff library loaded.");
      resolve(true);
    };
    script.onerror = () => {
      log("Failed to load diff library.", true);
      resolve(false);
    };
    document.head.appendChild(script);
  });
}

async function showDiff() {
  const container = document.getElementById("diffView");
  container.innerHTML = "";

  const loaded = await ensureDiffLibrary();
  if (!loaded) {
    container.style.display = "block";
    container.innerHTML = "Diff library failed to load. Cannot show diff.";
    return;
  }

  try {
    const dmp = new diff_match_patch();
    const edited = document.getElementById("editor").value;

    if (originalContent === edited) {
      container.style.display = "block";
      container.innerHTML = `<div style="color:#ccc;">No changes detected.</div>`;
      return;
    }

    const diffs = dmp.diff_main(originalContent, edited);
    dmp.diff_cleanupSemantic(diffs);

    diffs.forEach(([type, text]) => {
      const span = document.createElement("span");
      if (type === 1) span.style.background = "#144212";
      else if (type === -1) {
        span.style.background = "#5c1a1a";
        span.style.textDecoration = "line-through";
      }
      span.textContent = text;
      container.appendChild(span);
    });

    container.style.display = "block";
  } catch (err) {
    container.style.display = "block";
    container.innerHTML = `Error generating diff: ${err.message}`;
    log("Diff error: " + err.message, true);
  }
}

// ----------------- Submit -----------------
async function submitEdit() {
  try {
    if (!accessToken) {
      githubLogin();
      return;
    }

    const edited = document.getElementById("editor").value;
    if (originalContent === edited) {
      log("No changes detected.", true);
      return;
    }

    showDiff();
    if (!confirm("Submit these changes?")) return;

    log("Starting submission...");

    const user = await api("https://api.github.com/user");
    const username = user.login;
    const editOwnFork = document.getElementById("editOwnFork").checked;

    if (!editOwnFork) await ensureFork(username);

    const baseSha = await getUpstreamSha();
    const branchName = "edit-" + Date.now();

    await createBranch(username, branchName, baseSha);
    await commitFile(username, branchName);

    if (!editOwnFork) {
      const pr = await createPR(username, branchName);
      log(`PR created: <a href="${pr.html_url}" target="_blank">${pr.html_url}</a>`);
    } else {
      log("Changes committed to your fork branch.");
    }
  } catch (err) {
    log("Error: " + err.message, true);
    console.error(err);
  }
}

//NEw code
const STORAGE_KEY = "github_pat";

function openSelection(editUrl) {
  const overlay = document.getElementById("edit-modal-overlay");

  // Set links dynamically
  document.getElementById("edit-github").href = editUrl;

  // Customize these as needed
  const anonButton = document.getElementById("edit-anon");
  anonButton.onclick = function(e) {
    e.preventDefault();
    openEditor(editUrl);
  }

  const container = document.getElementById("pat-token-container");
  container.style.display = "none";

  const existingToken = loadToken();
  if(existingToken){
    container.style.display = "flex";
    const tokenInput = document.getElementById("pat-token-input");
    tokenInput.value = existingToken;
  }
  // Wire the token button to show input field
  const tokenButton = document.getElementById("edit-token");
  tokenButton.onclick = function(e) {
    e.preventDefault();

    const container = document.getElementById("pat-token-container");
    container.style.display = "flex";

    const tokenInput = document.getElementById("pat-token-input");
    const existingToken = loadToken();
    if (existingToken) {
      tokenInput.value = existingToken;
    }
  };
  overlay.style.display = "flex";
}

function closeSelection(event) {
  // Only close if clicking outside modal or explicitly called
  if (!event || event.target.id === "edit-modal-overlay") {
    document.getElementById("edit-modal-overlay").style.display = "none";
  }
}

function saveToken(token) {
  localStorage.setItem(STORAGE_KEY, token);
}

function loadToken() {
  return localStorage.getItem(STORAGE_KEY);
}

function clearToken() {
  localStorage.removeItem(STORAGE_KEY);
  document.getElementById("pat-token-input").value = "";
  alert("Token cleared");
}

// Save button
document.getElementById("save-pat").addEventListener("click", function() {
  const token = document.getElementById("pat-token-input").value.trim();
  if (!token) {
    alert("Please enter a token");
    return;
  }
  saveToken(token);
  alert("Token saved!");
});

// Clear button
document.getElementById("clear-pat").addEventListener("click", clearToken);