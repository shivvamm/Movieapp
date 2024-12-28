<template>
  <div class="movie-page bg-gray-900 text-white">
    <!-- Header -->
    <header
      class="relative bg-gray-800 bg-opacity-70 text-center p-6 flex flex-col items-center justify-between"
    >
      <!-- Backdrop as Header Background -->
      <div
        class="absolute inset-0 opacity-50"
        :style="{
          backgroundImage: `url(${movie.Poster})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }"
      ></div>

      <!-- Title Section -->
      <h1 class="text-3xl font-bold z-10">{{ movie.Title }}</h1>

      <!-- Button Section Below the Title -->
      <div class="mt-4 z-10 flex justify-center space-x-4">
        <button
          class="px-4 py-2 text-sm font-semibold bg-blue-600 rounded hover:bg-blue-500"
        >
          Like
        </button>
        <button
          class="px-4 py-2 text-sm font-semibold bg-green-600 rounded hover:bg-green-500"
        >
          Share
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
      <div class="poster">
        <img
          :src="movie.Poster"
          alt="Movie Poster"
          class="w-full h-auto rounded-lg shadow-lg transform transition-transform duration-300 hover:scale-105"
        />
      </div>

      <div class="details space-y-4">
        <p>
          <strong class="font-semibold">Release Date:</strong>
          {{ movie.Released }}
        </p>
        <p>
          <strong class="font-semibold">IMDB Rating:</strong>
          {{ movie.imdbRating }}
        </p>
        <p><strong class="font-semibold">Genre:</strong> {{ movie.Genre }}</p>
        <p><strong class="font-semibold">Plot:</strong> {{ movie.Plot }}</p>
        <p>
          <strong class="font-semibold">Director:</strong> {{ movie.Director }}
        </p>
        <p><strong class="font-semibold">Writer:</strong> {{ movie.Writer }}</p>
        <p><strong class="font-semibold">Actors:</strong> {{ movie.Actors }}</p>
        <p>
          <strong class="font-semibold">Language:</strong> {{ movie.Language }}
        </p>
        <p>
          <strong class="font-semibold">Country:</strong> {{ movie.Country }}
        </p>
        <p><strong class="font-semibold">Awards:</strong> {{ movie.Awards }}</p>
      </div>
    </main>

    <!-- Footer -->
    <footer class="text-center p-4 bg-gray-800 bg-opacity-70 mt-6">
      <button
        @click="openTrailer"
        class="relative px-6 py-2 text-white font-semibold bg-red-600 rounded hover:bg-red-500 transition-all overflow-hidden"
      >
        <span
          class="absolute inset-0 bg-red-700 opacity-0 hover:opacity-20 transition-opacity"
        ></span>
        <span class="z-10 relative">Watch Trailer</span>
        <span
          class="absolute w-full h-1 left-0 bottom-0 bg-yellow-400 animate-glow"
        ></span>
      </button>

      <!-- Trailer Modal -->
      <div
        v-if="showTrailer"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-80 z-50"
      >
        <iframe
          width="800"
          height="450"
          :src="`https://www.youtube.com/embed/${movieTrailerId}`"
          frameborder="0"
          allowfullscreen
          class="rounded-lg"
        ></iframe>
        <button
          @click="closeTrailer"
          class="absolute top-5 right-5 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-500"
        >
          Close
        </button>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      movie: {},
      showTrailer: false,
      movieTrailerId: "dW1BIid8Osg",
    };
  },
  methods: {
    openTrailer() {
      this.showTrailer = true;
    },
    closeTrailer() {
      this.showTrailer = false;
    },
  },
  async mounted() {
    const response = await fetch(
      "http://www.omdbapi.com/?i=tt3896198&apikey=d2132124"
    );
    this.movie = await response.json();
  },
};
</script>

<style scoped>
@keyframes glow {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

button:hover .animate-glow {
  animation: glow 2s infinite linear;
}

footer button {
  position: relative;
  overflow: hidden;
}
footer button span.absolute {
  background: rgba(255, 255, 255, 0.2);
}

/* Scoped Styles for Hover Effects */
.poster img:hover {
  transform: scale(1.05);
}

/* Add Background Gradient for Header */
header {
  position: relative;
  overflow: hidden;
}
header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.6),
    rgba(0, 0, 0, 0.8)
  );
  z-index: 1;
}
</style>
