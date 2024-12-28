// src/components/VideoPlay.vue
<template>
  <div class="video-modal">
    <iframe
      :src="'https://www.youtube.com/embed/' + videoId"
      frameborder="0"
      allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen
      class="w-full h-full"
    ></iframe>
    <button @click="$emit('close')" class="close-button">Close</button>
  </div>
</template>

<script>
export default {
  name: "VideoPlay",
  props: {
    videoId: String,
  },
};
</script>
