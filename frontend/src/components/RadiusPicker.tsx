
import * as React from 'react';
import { Autocomplete, Card, CardContent, CardMedia, TextField, Typography } from '@mui/material';
import { topCities } from '../const/topCities';
import { radiusOptions } from '../const/radiusOptions';

const RadiusPicker = ({ value, onPick }) => {
    return (

        <Autocomplete
            disablePortal
            options={radiusOptions}
            value={value}
            sx={{ width: 200 }}
            renderInput={(params) => <TextField {...params} label="Radius" />}
            onChange={(event, value) => { console.log(value); onPick(value) }}
        />

    );
};

export default RadiusPicker;