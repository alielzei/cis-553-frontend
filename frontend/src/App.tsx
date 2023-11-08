import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import axios from 'axios'; // You'll need Axios or another HTTP library for sending requests.
import { CircularProgress, Container, Grid } from '@mui/material';
import MovieCard from './MovieCard';

function App() {
  const [searchText, setSearchText] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {

    setLoading(true);
    setTimeout(() => {
      setSearchResults(['result 1', 'result 2', 'result 3', 'result 4', 'result 5']);
      setLoading(false);
    }, 500)

    // Make an HTTP request here using axios or your preferred HTTP library.
    // Replace the URL with your actual API endpoint.
    // try {
    //   const response = await axios.get(`https://your-api-endpoint.com/search?query=${searchText}`);
    //   const data = response.data;
    //   setSearchResults(data);
    // } catch (error) {
    //   console.error('Error:', error);
    // }
  };

  const handleEnterKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <Container
      className="flex flex-col p-4 pt-10 bg-blue-100 "
    >
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
          <CircularProgress />
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
                title="Your Movie Title"
                cast="Actor 1, Actor 2, Actor 3"
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
