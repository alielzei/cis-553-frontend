
import * as React from 'react';
import { Autocomplete, Card, CardContent, CardMedia, TextField, Typography } from '@mui/material';
import { topCities } from './topCities';


export const LocationPicker = ({ value, onPick }) => {
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

export const RadiusPicker = ({ value, onPick }) => {
    return (

        <Autocomplete
            disablePortal
            options={[{ label: "5 mi" }, { label: "10 mi" }, { label: "15 mi" }, { label: "30 mi" }]}
            value={value}
            sx={{ width: 200 }}
            renderInput={(params) => <TextField {...params} label="Radius" />}
            onChange={(event, value) => { console.log(value); onPick(value) }}
        />

    );
};

