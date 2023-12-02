import React, { useState } from 'react';

import axios from 'axios'; // You'll need Axios or another HTTP library for sending requests.

import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { CircularProgress, Container, Grid } from '@mui/material';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import MovieCard from './MovieCard';


axios.defaults.baseURL = "http://127.0.0.1:5000";

interface Suggestion {
  name: string;
  year: string;
  actors: string;
  desc: string;
}

interface Showtime {}

interface MovieSuggestionsResponse {
  suggestions: Suggestion[];
  showtimes: Showtime[];
}

function App() {
  const [searchText, setSearchText] = useState("Can you give me suggestions on movies about animals?");
  const [searchResults, setSearchResults] = useState<Suggestion[]>([]);
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
      const response = await axios.post<MovieSuggestionsResponse>('/', { question: searchText }, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      setSearchResults(response.data.suggestions);
    } catch (error) {
      console.log("something")
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
        // progress: ,
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
          {searchResults.map((result, index) => (
            <Grid item>
              <MovieCard
                imageUrl={`https://picsum.photos/seed/${index}abc/300/200`}
                title={result.name}
                cast={result.actors}
                showtime="8:00 PM"
                theaterName="Your Theater Name"
              />

            </Grid>
          ))}
        </Grid>

      </div>
    </Container>
  );
}

export default App;
