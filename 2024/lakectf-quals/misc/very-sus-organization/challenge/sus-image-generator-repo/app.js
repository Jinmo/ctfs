const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// API to get a random image
app.get('/random-image', (req, res) => {
    const imagesDir = path.join(__dirname, 'public', 'images');
    const images = fs.readdirSync(imagesDir); // Get all filenames in the images directory
    const randomImage = images[Math.floor(Math.random() * images.length)];
    res.json({ image: `/images/${randomImage}` });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
