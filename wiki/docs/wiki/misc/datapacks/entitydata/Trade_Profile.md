---
show:
  - toc
---

# **Trader Profile**

A trader profile defines the complete trading behavior for a custom NPC trader, including trade pools, trade counts, refresh logic, alignment requirements, and wandering behavior.

Trader profiles are fully data-driven and configured using JSON files. Each profile describes **what a trader buys**, **what they sell**, **how many trades they offer**, and **how those trades refresh over time**.

Trades are selected from weighted pools and may offer either fixed or randomized items and prices, allowing for highly configurable and replayable trader behavior.


Trader Profiles are defined and configured using JSON files located within a data pack under:  
- `data/<namespace>/trader_profiles/<profile>.json`  
- Where the `namespace` defines what mod is adding it and `profile` is the profile's id.

## Trader Profile JSON format
<div class="display-tree">
  <ul>
    <li>
      The root object
      <ul>
        <li><strong>id</strong>: <code>namespace:path</code> (required)
          <ul>
            <li>Unique identifier for this trader profile.</li>
            <li>An invalid or missing `id` value will cause the profile to fail loading</li>
            <li>Must match the file location of this entry. Located in <code>data/&lt;namespace&gt;/trader_profiles/&lt;path&gt;.json</code></li>
          </ul>
        </li>
        <li><strong>tradingAlignmentRequired</strong>: <code>int</code> (required)
          <ul>
            <li>Minimum alignment required to trade with this NPC.</li>
          </ul>
        </li>
        <li><strong>minimumTradesOffered</strong>: <code>int</code> (required)
          <ul>
            <li>The minimum number of trades this trader will offer.</li>
            <li>If `minimumTradesOffered + maximumAdditionalTradesOffered > 9`, minimumTradesOffered will be forcibly reset to <code>3</code>.</li>
          </ul>
        </li>
        <li><strong>maximumAdditionalTradesOffered</strong>: <code>int</code> (required)
          <ul>
            <li>Additional trades added randomly beyond the minimum.</li>
            <li>If `minimumTradesOffered + maximumAdditionalTradesOffered > 9`, maximumAdditionalTradesOffered will be forcibly reset to <code>6</code>.</li>
          </ul>
        </li>
        <li><strong>shouldRefreshTrades</strong>: <code>true|false</code> (required)
          <ul>
            <li>If true, the trader will refresh their trade list after a threshold is reached.</li>
            <li>Typicaly set to <code>true</code>.</li>
          </ul>
        </li>
        <li><strong>refreshTradesAtValue</strong>: <code>int</code> (required)
          <ul>
            <li>Total trade value required before trades refresh.</li>
            <li>Typicaly set to <code>5000</code> coins.</li>
          </ul>
        </li>
        <li><strong>lockTicksAfterRefresh</strong>: <code>int</code> (required)
          <ul>
            <li>Cooldown (in ticks) after refresh before new trades become available.</li>
            <li>Typicaly set to <code>6000</code> ticks, or 5 minutes.</li>
          </ul>
        </li>
        <li><strong>isTypicallyWandering</strong>: <code>true|false</code> (default: <code>false</code>)
          <ul>
            <li>Indicates if this trader is usually wandering, used internally for trader validation and error correcting.</li>
          </ul>
        </li>
        <li><strong>buyFromPlayer</strong>: A list of trade pool items
          <ul>
            <li>Defines what items the trader buys from the player. See below.</li>
          </ul>
        </li>
        <li><strong>sellToPlayer</strong>: A list of trade pool items
          <ul>
            <li>Defines what items the trader sells to the player. See below.</li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>


## Trade pool items

Each entry in `buyFromPlayer` or `sellToPlayer` represents a **weighted trade option**.

<div class="display-tree">
  <ul>
    <li>
      A trade pool item
      <ul>
        <li><strong>weight</strong>: <code>int</code> (default: <code>1</code>)
          <ul>
            <li>Controls how likely this trade is to be selected.</li>
          </ul>
        </li>
        <li><strong>maxTransferQuantity</strong>: <code>int</code> (default: <code>200</code>)
          <ul>
            <li>Maximum quantity that can be traded.</li>
          </ul>
        </li>
        <li><strong>shouldTradePersist</strong>: <code>true|false</code> (default: <code>true</code>)
          <ul>
            <li>If false, the trade is removed after use and not ticked back.</li>
            <li>Used for one-time available trades, like with smith scrolls.</li>
          </ul>
        </li>
        <li>
          One of below (required):
          <ul>
            <li><strong>stack</strong>: Single item definition</li>
            <li><strong>stacks</strong>: Multiple item definitions</li>
            <li>Either `stack` <strong>or</strong>`stacks` must be defined — <strong>never both</strong>!</li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>

## Item supplier formats

### **Single Stack Supplier** { #single_stack data-toc-label="Single Stack" }
Defines a trade that always uses the same item and price.

<div class="display-tree">
  <ul>
    <li>
      <strong>stack</strong>
      <ul>
        <li><strong>item</strong>: <code>namespace:item</code> (required)</li>
        <li><strong>averageCost</strong>: <code>int</code> (default: <code>1000</code>)</li>
        <li><strong>count</strong>: <code>int</code> (default: <code>1</code>)</li>
        <li><strong>nbt</strong>: <code>string</code> (optional)</li>
      </ul>
    </li>
  </ul>
</div>

### **Multi Stack Supplier** { #multi_stack data-toc-label="Multi Stack" }
Defines a trade that randomly selects from multiple possible items.

<div class="display-tree">
  <ul>
    <li>
      <strong>stacks</strong>: List of stack entries
      <ul>
        <li>Each entry follows the same format as a single stack</li>
        <li>One entry is chosen randomly per trade</li>
      </ul>
    </li>
  </ul>
</div>


## Example trader profile

```json title="data/lotrextended/trader_profiles/bree_brewer.json"
{
  "id": "lotrextended:bree_brewer",
  "tradingAlignmentRequired": 0,
  "minimumTradesOffered": 3,
  "maximumAdditionalTradesOffered": 6,
  "shouldRefreshTrades": true,
  "refreshTradesAtValue": 5000,
  "lockTicksAfterRefresh": 6000,
  "buyFromPlayer": [
    {
      "weight": 50,
      "stack": {
        "item": "minecraft:wheat",
        "averageCost": 1,
        "count": 2
      }
    },
    {
      "weight": 50,
      "stack": {
        "item": "minecraft:apple",
        "averageCost": 1
      }
    },
    {
      "weight": 50,
      "stack": {
        "item": "minecraft:potato",
        "averageCost": 1,
        "count": 2
      }
    }
  ],
  "sellToPlayer": [
    {
      "weight": 50,
      "stack": {
        "item": "lotr:apple_juice",
        "averageCost": 6
      }
    },
    {
      "weight": 50,
      "stack": {
        "item": "lotr:sweet_berry_juice",
        "averageCost": 5
      }
    },
    {
      "weight": 50,
      "stacks": [
        {
          "item": "lotr:ale",
          "averageCost": 8,
          "nbt": "{vessel:{potency:\"light\"}}"
        },
        {
          "item": "lotr:ale",
          "averageCost": 10,
          "nbt": "{vessel:{potency:\"moderate\"}}"
        },
        {
          "item": "lotr:ale",
          "averageCost": 12,
          "nbt": "{vessel:{potency:\"strong\"}}"
        }
      ]
    },
    {
      "weight": 50,
      "stack": {
        "item": "lotr:ceramic_mug",
        "averageCost": 2
      }
    }
  ]
}
```
