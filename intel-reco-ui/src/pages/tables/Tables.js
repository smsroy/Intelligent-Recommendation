import React, { useState, useEffect } from "react";
// import React from "react";
import { Grid } from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";
import MUIDataTable from "mui-datatables";
import Box from "@material-ui/core/Box";
import TextField from "@material-ui/core/TextField";
import MenuItem from "@material-ui/core/MenuItem";
import Button from "@material-ui/core/Button";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import Table from "../dashboard/components/Table/Table";

// data
import mock from "../dashboard/mock";

// const datatableData = [
//   ["Joe James", "Example Inc.", "Yonkers", "NY"],
//   ["John Walsh", "Example Inc.", "Hartford", "CT"],
//   ["Bob Herm", "Example Inc.", "Tampa", "FL"],
//   ["James Houston", "Example Inc.", "Dallas", "TX"],
//   ["Prabhakar Linwood", "Example Inc.", "Hartford", "CT"],
//   ["Kaui Ignace", "Example Inc.", "Yonkers", "NY"],
//   ["Esperanza Susanne", "Example Inc.", "Hartford", "CT"],
//   ["Christian Birgitte", "Example Inc.", "Tampa", "FL"],
//   ["Meral Elias", "Example Inc.", "Hartford", "CT"],
//   ["Deep Pau", "Example Inc.", "Yonkers", "NY"],
//   ["Sebastiana Hani", "Example Inc.", "Dallas", "TX"],
//   ["Marciano Oihana", "Example Inc.", "Yonkers", "NY"],
//   ["Brigid Ankur", "Example Inc.", "Dallas", "TX"],
//   ["Anna Siranush", "Example Inc.", "Yonkers", "NY"],
//   ["Avram Sylva", "Example Inc.", "Hartford", "CT"],
//   ["Serafima Babatunde", "Example Inc.", "Tampa", "FL"],
//   ["Gaston Festus", "Example Inc.", "Tampa", "FL"],
// ];

const categories = [
  {
    value: "Electronics",
    label: "electronics",
  },
  {
    value: "Ipads",
    label: "ipads",
  },
  {
    value: "TV",
    label: "tv",
  },
  {
    value: "Cellphones",
    label: "cellphones",
  },
];

const useStyles = makeStyles((theme) => ({
  tableOverflow: {
    overflow: "auto",
  },
}));

export default function Tables() {
  const [datatableData, setDatatableData] = useState([{}]);
  const classes = useStyles();

  const [keywords, setKeywords] = React.useState(" ");
  const handleKWChange = (event) => {
    setKeywords(event.target.value);
  };

  const [category, setCategory] = React.useState("electronics");
  const handleChange = (event) => {
    setCategory(event.target.value);
  };

  useEffect(() => {
    fetch("/search-result-queryarr")
      .then((res) => res.json())
      .then((data) => {
        setDatatableData(data);
        console.log(data);
      });
  }, []);

  return (
    <>
      <PageTitle title="Recommendation" />
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Widget
            title="Product Recommendation Search"
            upperTitle
            noBodyPadding
            bodyClass={classes.tableOverflow}
          >
            <Box
              component="form"
              sx={{
                "& > :not(style)": { m: 1, width: "25ch" },
              }}
              noValidate
              autoComplete="off"
            >
              <TextField
                id="key-words"
                label="Product Keywords"
                multiline
                maxRows={4}
                value={keywords}
                onChange={handleKWChange}
              />
              <TextField
                id="select-category"
                select
                label="Category"
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
              <Button variant="outlined">Get Recommendation</Button>
            </Box>
          </Widget>
        </Grid>
        <Grid item xs={12}>
          <MUIDataTable
            title="Recommendation List"
            data={datatableData}
            columns={["Title", "Rating", "Reviews", "Price", "Url"]}
            options={{
              filterType: "checkbox",
            }}
          />
        </Grid>
      </Grid>
    </>
  );
}
