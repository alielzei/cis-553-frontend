
import * as React from 'react';
import { Card, CardContent, CardMedia, Typography } from '@mui/material';

const MovieCard = ({ imageUrl, title, cast, showtime, theaterName }) => {
    return (
        <Card


            sx={{ width: 345 }}>
            <CardMedia
                component="img"
                image={imageUrl}
                alt={title}
            />
            <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                    {title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    <strong>Cast:</strong> {cast}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    <strong>Showtime:</strong> {showtime}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    <strong>Theater Name:</strong> {theaterName}
                </Typography>
            </CardContent>
        </Card>
    );
};

export default MovieCard;
