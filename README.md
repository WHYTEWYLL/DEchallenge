# DEchallenge

Practical
Please use Python for the following task.

Create an application that will:
Index every The Doge NFT (DOG) token Transfer event on the Ethereum Mainnet.
Be able to index the events using 2 strategies: continuously (following the latest block) and on-demand (index events based on a block range from [block number] to [block number]).
Process Transfer events - create an aggregation of token holders (list of token holders with their balance).
Prepare the data in a way that it can be consumed by the engineering team. The team will be:

Fetching token holder's balance
Fetching top 100 token holders - make sure to include what % of the total supply their balance represent
Fetching token holder's weekly balance change (in %)
The solution should be scalable to 100 million entries.

Write all needed tests.

Write a high-level description (1 page) explaining your solution. Explanation should include:

A description of what you've built
Which technologies you've used and how they tie together
Your reasons for high-level decisions and potential improvements, bottlenecks and performance estimates
