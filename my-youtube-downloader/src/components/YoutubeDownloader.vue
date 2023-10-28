<template>
  <div>
    <h1>YouTube Downloader</h1>
    <input v-model="url" placeholder="Enter YouTube URL" />
    <button @click="downloadVideo">Download Video</button>
    <button @click="downloadAudio">Download Audio</button>
   
    <button @click="getVideoInfo">Download and Display Info</button>
    <div v-if="info">
      <h3>Video Title: {{ info.title }}</h3>
      <img :src="info.thumbnail_url" alt="Thumbnail" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      url: '',
      quality: 'best',
      audioQuality: '192',
      info: null
    };
  },
  methods: {
    async downloadVideo() {
      const response = await fetch('http://localhost:8000/download_video', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: this.url,
          quality: this.quality
        })
      });
      if (response.ok) {
        alert('Video downloaded successfully');
      } else {
        alert('Error downloading video');
      }
    },
    async downloadAudio() {
      const response = await fetch('http://localhost:8000/download_audio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: this.url,
          audio_quality: this.audioQuality
        })
      });
      if (response.ok) {
        alert('Audio downloaded successfully');
      } else {
        alert('Error downloading audio');
      }
    },
    async getVideoInfo() {
      try {
        const response = await fetch(`http://localhost:8000/get_video_info?url=${encodeURIComponent(this.url)}`, {
          method: 'GET'
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.info = await response.json();
      } catch (error) {
        console.error('There was a problem with the fetch:', error);
      }
    }
  }
};
</script>
