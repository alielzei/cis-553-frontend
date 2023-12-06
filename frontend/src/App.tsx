import React, { useState } from 'react';

import axios from 'axios'; // You'll need Axios or another HTTP library for sending requests.

import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { CircularProgress, Container, Grid, Typography } from '@mui/material';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import MovieCard from './components/MovieCard';
import ShowtimeCard from './components/ShowtimeCard';
import LocationPicker from './components/LocationPicker';
import RadiusPicker from './components/RadiusPicker';
import { City, topCities } from './const/topCities';
import { radiusOptions } from './const/radiusOptions';

import mockdata from './mockdata.json';

axios.defaults.baseURL = "https://cis-553-project-166e10ea0d1c.herokuapp.com";

interface Suggestion {
  name: string;
  year: string;
  actors: string;
  desc: string;
}

interface Theater {
  distance: string;
  name: string;
  times: Array<string>;
}

interface Showtime {
  details: Array<string>;
  movie_name: string;
  image: string;
  showtimes: Theater[];
}

interface MovieSuggestionsResponse {
  suggestions: Suggestion[];
  showtimes: Showtime[];
}

function App() {
  const [searchText, setSearchText] = useState("Do you have any horror movie suggestions currently in theaters?");
  const [searchResults, setSearchResults] = useState<MovieSuggestionsResponse>({ suggestions: [], showtimes: [] });
  const [selectedLocation, setSelectedLocation] = useState<City>(topCities[0]); // topCities[0
  const [selectedRadius, setSelectedRadius] = useState(radiusOptions[0]); // topCities[0

  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {

    setLoading(true);
    // setTimeout(() => {
    //   setSearchResults(['result 1', 'result 2', 'result 3', 'result 4', 'result 5']);
    //   setLoading(false);
    // }, 500)

    // Make an HTTP request here using axios or your preferred HTTP library.
    // Replace the URL with your actual API endpoint.
    try {
      console.log(selectedLocation?.city, selectedLocation?.state, selectedRadius)
      const response = await axios.post<MovieSuggestionsResponse>('/', {
        question: searchText,
        city: selectedLocation?.city || null,
        state: selectedLocation?.state || null,
        radius: selectedRadius?.value || null,
      }, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      setSearchResults(response.data);
      // setSearchResults(mockdata);
    } catch (error) {
      toast.error(<>
        <div>We are sorry!</div>
        <div>Our application is down due technical issues, we are trying our best to fix it as early as possible.</div>
        <div>Appreciate  your patience!</div>
      </>,
        {
          position: "top-center",
          autoClose: 4000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          theme: "colored",
        });
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEnterKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <Container
      className="flex flex-col p-4 pt-10"
    >
      <ToastContainer />

      <div className="flex flex-row gap-2 mb-8">
        <div className="grow">
          <Typography variant="h3" >MovieMate - your buddy for anything movie!</Typography>
          <Typography variant="h5" >Tell us what's on your mind today</Typography>
        </div>
        <LocationPicker value={selectedLocation} onPick={setSelectedLocation} />
        <RadiusPicker value={selectedRadius} onPick={setSelectedRadius} />
      </div>
      <div
        className="flex flex-row gap-2"
      >
        <TextField
          label="Search"
          variant="outlined"
          fullWidth
          className='grow'
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          onKeyPress={handleEnterKeyPress}
        />
        <Button variant="contained" onClick={handleSearch}>
          Search
        </Button>
      </div>
      <div
        className="pt-4"
      >

        {loading && <div className="flex justify-center items-center h-full">
          <div className="flex flex-col p-4 pb-8 justify-center items-center">
            <p className="p-4">
              Fetching movie suggestions...
            </p>
            <CircularProgress />
          </div>
        </div>}

        <Grid container
          wrap='nowrap'
          sx={{ overflow: "auto" }} // --> add scrollbar when the content inside is overflowed
          spacing={2}

        >
          {searchResults.showtimes.map((showtime, i1) => {
            showtime.showtimes = showtime.showtimes.flat(Infinity)
            return showtime.showtimes.map((time, i2) => (
              <Grid item key={`${i1 - i2}`}>
                <ShowtimeCard
                  imageUrl={showtime.image}
                  title={showtime.movie_name}
                  showtime={time.times?.join(" ") || "N/A"}
                  theaterName={time.name || "N/A"}
                  distance={time.distance || "N/A"}
                />
              </Grid>
            ))
          })}

          {searchResults.suggestions.map((result, index) => (
            <Grid item key={index}>
              <MovieCard
                imageUrl={`https://picsum.photos/seed/${index}abc/300/200`}
                title={result.name}
                cast={result.actors}
              />

            </Grid>
          ))}
        </Grid>

      </div>
    </Container>
  );

}

export default App;
