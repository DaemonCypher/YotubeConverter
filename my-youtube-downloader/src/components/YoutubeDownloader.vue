<template>
  <div>
    <h1>YouTube Downloader</h1>
    <div class="parent-container">
    <div class="input-container">
      <input class="url-input" v-model="url" placeholder="Enter YouTube URL" />
      <button class="action-button" @click="getVideoInfo">
        <img src="../assets/search.svg" alt="Download and Display Info" />
      </button>
    </div>
  </div>
    <button class="action-button" @click="downloadVideo">Download Video</button>
      <button class="action-button" @click="downloadAudio">Download Audio</button>
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
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    // the filename you want
    a.download = 'video.mp4'; 
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
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
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    // the filename you want
    a.download = 'audio.mp3'; 
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
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
