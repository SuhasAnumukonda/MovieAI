

homeHTML = `
<div class = "home">
    <p class = "header"><b>Welcome to Movie<span>AI</span>!</b></p>
    <p class = "headerSubText">MovieAI is a website that allows you search for movies, and an AI will analyze movie reviews and ratings made by real humans</p>

    <p class = "sectionTitle">Movie Information:</p>
    <p class = "intro">After you search for a movie, you will see information about the movie, such as its <span>release information, genres, actors, and writers</span></p>

    <p class = "sectionTitle">Rating Information:</p>
    <p class = "intro">You will also see rating information, like its <span>stars out of ten</span> and <span>popularity</span></p>
    <p class = "intro">Popularity is a statistic that determines how popular a movie is based on its <span>ratings, views, bookmarks per day</span></p>

    <p class = "sectionTitle">Review Information:</p>
    <p class = "intro">The review information section provides <span>analysis of reviews</span> left by real people</p>
    <p class = "intro">The AI will tell you how many reviews are positive versus how many reviews are negative</p>
    <p class = "intro">Based on all the positive and negative reviews, the movie is given an <span>ML score</span>, which determines <span>how a movie is perceived based on user reviews</span></p>
    <ul class="mlscore">
        <li class = "intro">If a movie has an ML score between <span>0 and 0.25</span>, then the movie is <span>horrible</span></li>
        <li class = "intro">If a movie has an ML score between <span>0.25 and 0.45</span>, then the movie is <span>bad</span></li>
        <li class = "intro">If a movie has an ML score between <span>0.45 and 0.55</span>, then the movie is <span>average</span></li>
        <li class = "intro">If a movie has an ML score between <span>0.55 and 0.75</span>, then the movie is <span>great</span></li>
        <li class = "intro">If a movie has an ML score between <span>0.75 and 1</span>, then the movie is <span>exceptional</span></li>
    </ul>
    <p class = "intro">The AI also information about <span>word frequencies</span> and <span>bigram frequencies</span> in reviews</p>
    <p class = "sectionTitle">Additional Information:</p>
    <p class = "intro">The additional information section has <span>keywords</span> that relate to the movie, and <span>similar movies</span> to what you search</p>

    <p class = "note">Note: Movie information comes from the OMDB API, and rating, review, and additional information comes from TMDB. 
        Certain films, such as old, international, or unpopular films may have limited or no information</p>
</div>
`;

const movieSearchBox = document.getElementById('movie-search-box');
const searchList = document.getElementById('search-list');
const resultGrid = document.getElementById('result-grid');

resultGrid.innerHTML = homeHTML;

async function loadHome(){
    resultGrid.innerHTML = homeHTML;
}

// load movies from API
async function loadMovies(searchTerm){
    const URL = `https://omdbapi.com/?s=${searchTerm}&type=movie&page=1&apikey=addyourownAPIkey`;
    const res = await fetch(`${URL}`);
    const data = await res.json();
    if(data.Response == "True") displayMovieList(data.Search);
}

function findMovies(){
    let searchTerm = (movieSearchBox.value).trim();
    if(searchTerm.length > 0){
        searchList.classList.remove('hide-search-list');
        loadMovies(searchTerm);
    } else {
        searchList.classList.add('hide-search-list');
    }
}

function displayMovieList(movies){
    searchList.innerHTML = "";
    for(let idx = 0; idx < movies.length; idx++){
        let movieListItem = document.createElement('div');
        movieListItem.dataset.id = movies[idx].imdbID;
        movieListItem.classList.add('search-list-item');
        if(movies[idx].Poster != "N/A")
            moviePoster = movies[idx].Poster;
        else 
            moviePoster = "image_not_found.png";

        movieListItem.innerHTML = `
        <div class = "search-item-thumbnail">
            <img src = "${moviePoster}">
        </div>
        <div class = "search-item-info">
            <h3>${movies[idx].Title}</h3>
            <p>${movies[idx].Year}</p>
        </div>
        `;
        searchList.appendChild(movieListItem);
    }
    loadMovieDetails();
}

function loadMovieDetails(){
    const searchListMovies = searchList.querySelectorAll('.search-list-item');
    searchListMovies.forEach(movie => {
        movie.addEventListener('click', async () => {
            searchList.classList.add('hide-search-list');
            movieSearchBox.value = "";
            const result = await fetch(`http://www.omdbapi.com/?i=${movie.dataset.id}&apikey=addyourownAPIkey&type=movie`);
            const movieDetails = await result.json();
            resultGrid.innerHTML = 
            `<div class="loader-container">
                <div class="loader"></div>
            </div>`;
            
            fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(movieDetails.Title), 
                })
                .then(response => response.json())
                .then(data => {
                    displayMovieDetails(movieDetails, data);
                })

                .catch(error => {
                    console.error('Error', error);
                })


        });
    });
}

function displayMovieDetails(details, data){
    resultGrid.innerHTML = `
    <div class = "result-grid">

    <div class = "movie-poster">
        <img src = "${(details.Poster != "N/A") ? details.Poster : "image_not_found.png"}" alt = "movie poster">
    </div>
    <div class = "movie-info">
        <h3 class = "movie-title">${details.Title}</h3>
        <ul class = "movie-misc-info">
            <li class = "year">Year: ${details.Year}</li>
            <li class = "rated">Ratings: ${details.Rated}</li>
            <li class = "released">Released: ${details.Released}</li>
        </ul>
        <p class = "genre"><b>Genre:</b> ${details.Genre}</p>
        <p class = "writer"><b>Writers:</b> ${details.Writer}</p>
        <p class = "actors"><b>Actors: </b>${details.Actors}</p>
        <p class = "plot"><b>Plot:</b> ${details.Plot}</p>
        <p class = "language"><b>Language:</b> ${details.Language}</p>
        <p class = "awards"><b><i class = "fas fa-award"></i></b> ${details.Awards}</p>
        <p class = 
    </div>

    </div>
    `;

    if(data.dataAvailable === "none"){
        resultGrid.innerHTML += `
        <div class = "result-grid">

        <div class = "movie-info">
            <h1 class = "ratingTitle"><b>Rating Information</b></h1>
            <h3 class = "noData"><b>Sorry, no rating data available</b></h3>
            <h1 class = "reviewTitle"><b>Review Information</b></h1>
            <h3 class = "noData"><b>Sorry, no review data available</b></h3>
            <h1 class = "additionalInfoTitle"><b>Additional Information</b></h1>
            <h3 class = "noData"><b>Sorry, no additional data available</b></h3>
        </div>

        </div>
        `;
    }

    else if(data.dataAvailable === "limited"){
        resultGrid.innerHTML += `
        <div class = "result-grid">

        <div class = "movie-info">
            <h1 class = "ratingTitle"><b>Rating Information</b></h1>
            <p class = "popularity"><b>Popularity:</b> ${data.popularity}</p>
            <p class = "stars"><b>Stars:</b> ${data.stars}/10 from <b>${data.totalVotes}</b> votes</p>
            <h1 class = "reviewTitle"><b>Review Information</b></h1>
            <h3 class = "noData"><b>Sorry, no review data available</b></h3>
            <h1 class = "additionalInfoTitle"><b>Additional Information</b></h1>
            <p class = "keywords"><b>Keywords:</b> ${data.keywords}</p>
            <p class = "recommendations"><b>Similar Movies:</b> ${data.recommendations}</p>

        </div>

        </div>
        `;
    }

    else if(data.dataAvailable === "full"){
        const averageReviewNumber = parseFloat(data.averageReview);
        let averageReviewSentiment = "";
        if(averageReviewNumber < 0.25){
            averageReviewSentiment = "horrible";
        }
        else if(averageReviewNumber < 0.45){
            averageReviewSentiment = "bad";
        }
        else if(averageReviewNumber < 0.55){
            averageReviewSentiment = "average";
        }
        else if(averageReviewNumber < 0.75){
            averageReviewSentiment = "great";
        }
        else{
            averageReviewSentiment = "exceptional";
        };

        let AveragefromRating = "";
        if(data.averageRating === "Sorry, no average rating available"){
            AveragefromRating = data.averageRating;
        }
        else{
            AveragefromRating = ` </b>${data.averageRating}/10 from ${data.ratingLength} reviews`;
        }



        resultGrid.innerHTML += `
        <div class = "result-grid">

        <div class = "movie-info">
            <h1 class = "ratingTitle"><b>Rating Information</b></h1>
            <p class = "popularity"><b>Popularity:</b> ${data.popularity}</p>
            <p class = "stars"><b>Stars:</b> ${data.stars}/10 from <b>${data.totalVotes}</b> votes</p>
            <h1 class = "reviewTitle"><b>Review Information</b></h1>
            <p class = "numberofReviews"><i>Note: this analysis is based off ${data.numberofReviews} reviews</i></p>
            <p class = "averageRating"><b>Average Rating From Reviews: ${AveragefromRating}</p>
            <p class = "averageReview">With an ML score of <b>${data.averageReview}</b>, this movie is <b>${averageReviewSentiment}</b></p>
            <h1 class = "additionalInfoTitle"><b>Additional Information</b></h1>
            <p class = "keywords"><b>Keywords:</b> ${data.keywords}</p>
            <p class = "recommendations"><b>Similar Movies:</b> ${data.recommendations}</p>
        </div>
       
        <div>
            <canvas id="sentpieChart"></canvas>
            <canvas id="freqbarChart"></canvas>
            <canvas id="bigramsbarChart"></canvas>
        </div>

        
        </div> 
        `;

        const sentiments = JSON.parse(data.sentiments);
        const sentX = ["Positive", "Negative"];
        const sentY = [sentiments.positive, sentiments.negative]
        const sentCTX = document.getElementById('sentpieChart').getContext('2d');
        const sentChart = new Chart(sentCTX, {
            type: 'pie',
            data:{
                labels: sentX,
                datasets: [{
                    label: 'Reviews',
                    data: sentY,
                    backgroundColor: ['rgba(0, 153, 0, 1)', 'rgba(153, 0, 0, 1)'],
                    borderWidth: 0
                }]
            },
            options:{
                plugins:{
                    title:{
                        display: true,
                        text: 'Positive vs Negative Reviews'
                    }
                }
            }
        });

        const freq = JSON.parse(data.freq);
        const bigrams = JSON.parse(data.bigrams);
        let freqX = [];
        let freqY = [];
        let bigramsX = [];
        let bigramsY = [];
        
        let forLoopLength = 10;
        if(bigrams.length < 10 || freq.length < 10){
            forLoopLength = 3;
        }
        else if(bigrams.length < 3 || freq.length < 3){
            forLoopLength = 1;
        }

        for(i = 0; i < forLoopLength; i++){
            freqX.push(freq[i][0]);
            freqY.push(freq[i][1]);
            bigramsX.push(bigrams[i][0]);
            bigramsY.push(bigrams[i][1]);
        }
        const freqCTX = document.getElementById('freqbarChart').getContext('2d');
        const freqChart = new Chart(freqCTX, {
            type: 'bar',
            data:{
                labels: freqX,
                datasets: [{
                    label: 'Words',
                    data: freqY,
                    backgroundColor: 'rgba(0, 0, 153, 0.9)',
                    borderColor: 'rgba(0, 0, 153, 1)',
                    borderWidth: 1
                }]
            },
            options:{
                plugins:{
                    title:{
                        display: true,
                        text: 'Word Frequency'
                    }
                },
                scales:{
                    y:{
                        display: true,
                        beginAtZero: true,
                        title:{
                            display: true,
                            text: 'Number of Times a Word Appears',
                        }
                    }
                }
            }
        });

        const bigramsCTX = document.getElementById('bigramsbarChart').getContext('2d');
        const bigramsChart = new Chart(bigramsCTX, {
            type: 'bar',
            data:{
                labels: bigramsX,
                datasets: [{
                    label: 'Word Pairs',
                    data: bigramsY,
                    backgroundColor: 'rgba(76, 0, 153, 0.9)',
                    borderColor: 'rgba(76, 0, 153, 1)',
                    borderWidth: 1
                }]
            },
            options:{
                animation: {
                    tension: {
                      duration: 1000,
                      easing: 'linear',
                      from: 1,
                      to: 0,
                      loop: false,
                    }
                },
                plugins:{
                    title:{
                        display: true,
                        text: 'Bigrams Frequency',
                    }
                },
                scales:{
                    y:{
                        beginAtZero: true,
                        title:{
                            display: true,
                            text: 'Number of Times a Bigram Appears',
                        }

                    }
                },

            }
        });
    }

}


window.addEventListener('click', (event) => {
    if(event.target.className != "form-control"){
        searchList.classList.add('hide-search-list');
    }
});
