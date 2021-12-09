import React, { useState, useEffect } from "react";
import Chart from "react-google-charts";
import {
  Grid,
  LinearProgress,
  Select,
  OutlinedInput,
  MenuItem,
  Button,
} from "@material-ui/core";
import { useTheme } from "@material-ui/styles";
import {
  ResponsiveContainer,
  ComposedChart,
  AreaChart,
  LineChart,
  Line,
  Area,
  PieChart,
  Pie,
  Cell,
  YAxis,
  XAxis,
} from "recharts";

// styles
import useStyles from "./styles";

// components
import mock from "./mock";
import Widget from "../../components/Widget";
import PageTitle from "../../components/PageTitle";
import { Typography } from "../../components/Wrappers";
import TextField from "@material-ui/core/TextField";

const categories = [
  {
    value: "laptop",
    label: "laptop",
  },
  {
    value: "hoodies",
    label: "hoodies",
  },
  {
    value: "ipad",
    label: "ipad",
  },
  {
    value: "television",
    label: "television",
  },
  {
    value: "camera",
    label: "camera",
  },
  {
    value: "cellphone",
    label: "cellphone",
  },
  {
    value: "drone",
    label: "drone",
  },
  {
    value: "smartwatch",
    label: "smartwatch",
  },
  {
    value: "monitor",
    label: "monitor",
  },
  {
    value: "guitar",
    label: "guitar",
  },
  {
    value: "headphone",
    label: "headphone",
  },
  {
    value: "speaker",
    label: "speaker",
  },
];

export default function Dashboard(props) {
  var classes = useStyles();
  var theme = useTheme();

  // local
  //var [mainChartState, setMainChartState] = useState("monthly");
  const [statsData, setStatsData] = useState([{}]);
  const [totalProducts, setTotalProducts] = useState(0);
  const [totalCategories, setTotalCategories] = useState(0);
  // const [loaded, setLoaded] = useState(0);
  const [eucData, setEucData] = useState([{}]);

  const [category, setCategory] = React.useState("drone");
  const handleChange = (event) => {
    console.log("handleChange called");
    setCategory(event.target.value);
    eucDist();
  };

  const productStats = async (e) => {
    try {
      const result = await searchStats();
      let statData = [];
      let prCount = 0;
      let catCount = 0;
      const hdr = ["Category", "By No Of Products"];
      statData.push(hdr);
      if (result) {
        result.forEach((element) => {
          let arr = [];
          catCount++;
          arr.push(element[0]);
          arr.push(element[1]);
          prCount = prCount + element[1];
          statData.push(arr);
        });
        setStatsData(statData);
        setTotalProducts(prCount);
        setTotalCategories(catCount);
        // setLoaded(1);
        //console.log(statData);
      }
    } catch (error) {}
  };

  const searchStats = async () => {
    try {
      const result = await fetch(`/search-result-stats`).then((res) =>
        res.json(),
      );
      return result;
    } catch (error) {
      throw new Error(error.message);
    }
  };

  const eucDist = async (e) => {
    try {
      const result = await euclideanDistance(category);
      let euData = [];
      const hdr = ["Products", "Euclidean Distance"];
      euData.push(hdr);
      if (result) {
        result.forEach((element) => {
          let arr = [];
          arr.push(element[0]);
          arr.push(element[1]);
          euData.push(arr);
          console.log("eu", arr);
        });
        setEucData(euData);
        // setLoaded(1);
        console.log("euData", euData);
      }
    } catch (error) {}
  };

  const euclideanDistance = async (category) => {
    try {
      const result = await fetch(
        `/euclidean-product-distance/${category}`,
      ).then((res) => res.json());
      return result;
    } catch (error) {
      throw new Error(error.message);
    }
  };

  useEffect(() => {
    console.log("UseEffect Called");
    productStats();
    eucDist();
  }, []);

  return (
    <>
      <PageTitle title="Dashboard" />
      <Grid container spacing={4}>
        <Grid item lg={6} md={4} sm={6} xs={12}>
          <Widget
            title="Categories Overview"
            upperTitle
            bodyClass={classes.fullHeightBody}
            className={classes.card}
          >
            <div className={classes.visitsNumberContainer}>
              <Chart
                width={"600px"}
                height={"400px"}
                chartType="PieChart"
                loader={<div>Loading Chart</div>}
                data={statsData}
                options={{
                  title: "By Number of Products",
                  // Just add this option
                  is3D: true,
                }}
                rootProps={{ "data-testid": "2" }}
                onClick={eucDist}
              />
            </div>
            <Grid
              container
              direction="row"
              justify="space-between"
              alignItems="center"
            >
              <Grid item xs={4}>
                <Typography color="text" colorBrightness="secondary" noWrap>
                  Total Products #
                </Typography>
                <Typography size="md">{totalProducts}</Typography>
              </Grid>
              <Grid item xs={4}>
                <Typography color="text" colorBrightness="secondary" noWrap>
                  Categories #
                </Typography>
                <Typography size="md">{totalCategories}</Typography>
              </Grid>
              <Grid item xs={4}>
                <Typography color="text" colorBrightness="secondary" noWrap>
                  Default Reco #
                </Typography>
                <Typography size="md">10</Typography>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
        <Grid item lg={6} md={8} sm={6} xs={12}>
          <Widget
            title="Product Text Similarity: Euclidean Distance"
            upperTitle
            className={classes.card}
            bodyClass={classes.fullHeightBody}
          >
            <Chart
              width={"600px"}
              height={"400px"}
              chartType="Scatter"
              loader={<div>Loading Chart</div>}
              data={eucData}
              options={{
                // Material design options
                chart: {
                  title:
                    "Distance comparing various texts of products in a category",
                  subtitle:
                    "All distances are relative to the first product in the category which is at the origin",
                },
                hAxis: { title: "Products" },
                vAxis: { title: "Distance" },
              }}
              rootProps={{ "data-testid": "3" }}
            />
            <Grid item xs={12}>
              <TextField
                className={classes.field}
                required
                id="select-category"
                select
                label="Category"
                color="primary"
                variant="outlined"
                value={category}
                onChange={handleChange}
                helperText="Please select product category"
              >
                {categories.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
          </Widget>
        </Grid>
      </Grid>
    </>
  );
}

// #######################################################################
function getRandomData(length, min, max, multiplier = 10, maxDiff = 10) {
  var array = new Array(length).fill();
  let lastValue;

  return array.map((item, index) => {
    let randomValue = Math.floor(Math.random() * multiplier + 1);

    while (
      randomValue <= min ||
      randomValue >= max ||
      (lastValue && randomValue - lastValue > maxDiff)
    ) {
      randomValue = Math.floor(Math.random() * multiplier + 1);
    }

    lastValue = randomValue;

    return { value: randomValue };
  });
}

function getMainChartData() {
  var resultArray = [];
  var tablet = getRandomData(31, 3500, 6500, 7500, 1000);
  var desktop = getRandomData(31, 1500, 7500, 7500, 1500);
  var mobile = getRandomData(31, 1500, 7500, 7500, 1500);

  for (let i = 0; i < tablet.length; i++) {
    resultArray.push({
      tablet: tablet[i].value,
      desktop: desktop[i].value,
      mobile: mobile[i].value,
    });
  }

  return resultArray;
}
