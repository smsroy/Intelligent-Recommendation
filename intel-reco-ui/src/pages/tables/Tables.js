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
    value: "Laptop",
    label: "laptop",
  },
  {
    value: "ipad",
    label: "ipad",
  },
  {
    value: "hoodies",
    label: "hoodies",
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
  field: {
    marginTop: 20,
    marginBottom: 20,
    alignSelf: 'flex-end'
  },
  root: {
    justifyContent: 'center'
}


}));

export default function Tables() {
  const [datatableData, setDatatableData] = useState([{}]);
  const classes = useStyles();

  const [keywords, setKeywords] = React.useState("");
  const handleKWChange = (event) => {
    setKeywords(event.target.value);
  };

  const [category, setCategory] = React.useState("");
  const handleChange = (event) => {
    setCategory(event.target.value);
  };

  const searchProducts = async (e) => {
    try {
      const result = await search(keywords, category);

      if (result) {
        setDatatableData(result);
        console.log(result);
      }
    }
    catch (error) {

    }
  }

  const search = async (keywords, category) => {
    try {
      const result = await fetch(`/search-result-queryarr/${keywords}/${category}`)
      .then(res => res.json());
      console.log(result);
      return result;
    } catch (error) {
      throw new Error(error.message);
    }
  }

  // useEffect(() => {
  //   fetch("/search-result-queryarr")
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setDatatableData(data);
  //       console.log(data);
  //     });
  // }, []);

  return (
    <>
      <PageTitle title="Discover Recommended Products" />
      <Grid container spacing={4} justify="center" className="App">
        <Grid item xs={12} >
          <Widget
            title="Search by Product Category"
            upperTitle
            noBodyPadding
            bodyClass={classes.tableOverflow}
          >
            <Box pl={2} pr={2} pb={1} pt={1}
              component="form"
              sx={{
                "& > :not(style)": { m: 1, width: "25ch" },
              }}
              noValidate
              autoComplete="off"
            >  
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
              <TextField
                className={classes.field}
                required
                id="key-words"
                label="Product Keywords"
                multiline
                maxRows={4}
                color="primary"
                variant="outlined"
                value={keywords}
                onChange={handleKWChange}
                helperText="Please enter keywords"
              />
             <Grid> <Button variant="contained" color="primary" onClick={searchProducts}>Recommend</Button> </Grid>
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
