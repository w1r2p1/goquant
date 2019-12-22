[![codecov](https://codecov.io/gh/hyu2707/goquant/branch/master/graph/badge.svg)](https://codecov.io/gh/hyu2707/goquant)
![](https://github.com/hyu2707/goquant/workflows/.github/workflows/pythonapp.yml/badge.svg)
# goquant-trading
Send order to different broker. (Support IB and Alpaca right now)

## Current Status
```diff
+ US stock data source: Alpaca
+ US stock trading platform: Alpaca
+ US Bitcoin data source: Binance
+ US Bitcoin trading platform: Binance
- CN data source: None
- CN trading platfoorm: None
```


## Use Guide
Step 1. Create private config in `config/priv.yaml`
register free account in Alpaca
follow this format:
```
alpaca:
  id: "<YOUR_ID>"
  key: "<YOUR_KEY>"
```
Step 2. Build env
```
make install
```
then activate env:
```bash
source env/bin/activate
```
Step 3. Check tests
```bash
make test
```

## Dev Guide
### Test
```bash
make test
```
### Lint
```bash
make lint
```

