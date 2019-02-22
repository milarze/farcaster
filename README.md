# farcaster

#### Gist
Builds a docker image that reads a json input from a file URL and generates a forecasted based on that time series.
Uses `statsmodels` library.

### Usage
Build Docker image
```
bin/build-docker-image
```

Run docker
```
docker run -e INPUT_JSON_URL=file_url farcaster
```

Input JSON file format
```
{
  "time_series": [
    {
      "date": "2019-02-21",
      "quantity":20.0
    }
    ...
  ],
  "aggregation": "day" // day, week or month
}
```
