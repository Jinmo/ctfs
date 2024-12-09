function getRandomSuspiciousNumber(max) {
    if (typeof max !== 'number' || max <= 0) {
        throw new Error('Max value must be a positive number.');
    }

    // Convert "sus" to an integer
    const susValue = "sus".split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);

    // Generate a random number and apply the modulo operation
    const randomBase = Math.floor(Math.random() * max);
    return (randomBase + susValue) % max;
}

module.exports = {
    getRandomSuspiciousNumber,
};
