
import * as React from 'react';
import { Autocomplete, Card, CardContent, CardMedia, TextField, Typography } from '@mui/material';
import { topCities } from '../const/topCities';


const LocationPicker = ({ value, onPick }) => {
    return (
        <>
            <Autocomplete
                disablePortal
                options={topCities}
                value={value}
                sx={{ width: 300 }}
                renderInput={(params) => <TextField {...params} label="Location" />}
                onChange={(event, value) => { console.log(value); onPick(value) }}
            />

        </>
    );
};

export default LocationPicker;
