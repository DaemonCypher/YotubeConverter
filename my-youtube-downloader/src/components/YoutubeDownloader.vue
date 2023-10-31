<template>
  <div>
    <h1>YouTube Downloader</h1>
    <div class="parent-container">
      <div class="input-container">
        <input
          class="url-input"
          v-model="url"
          placeholder="Enter YouTube URL"
          @keyup.enter="getVideoInfo" 
        />
        <button class="action-button" @click="getVideoInfo">
          <img src="../assets/search.svg" alt="Download and Display Info" />
        </button>
      </div>
      
      <!-- Quality Selection Dropdowns -->
      <div class="quality-selection">
        <label for="video-quality">Video Quality:</label>
        <select id="video-quality" v-model="quality">
          <option value="best">Best</option>
          <option value="2160">2160p</option>
          <option value="1440">1440p</option>
          <option value="1080">1080p</option>
          <option value="720">720p</option>
          <option value="480">480p</option>
          <option value="360">360p</option>
          <option value="240">240p</option>
          <option value="144">144p</option>
        </select>

        <label for="audio-quality">Audio Quality:</label>
        <select id="audio-quality" v-model="audioQuality">
          <option value="320">Exceptional (320 kbps)</option>
          <option value="256">High (256 kbps)</option>
          <option value="192">Medium (192 kbps)</option>
          <option value="128">Low (128 kbps)</option>
        </select>
      </div>
    </div>
  
    <div v-if="info">
      <h3>Video Title: {{ info.title }}</h3>
      <img :src="info.thumbnail_url" alt="Thumbnail" />
      <br>
      <button class="action-button" @click="downloadVideo">Download Video</button>
      <button class="action-button" @click="downloadAudio">Download Audio</button>
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
      alert(this.quality);
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
        const contentDisposition = response.headers.get('Content-Disposition');
        let fileName = 'download.mp4';  // Default file name
        if (contentDisposition) {
          const match = contentDisposition.match(/filename="(.+)"/);
          if (match && match[1]) {
            fileName = match[1];
          }
        }
        a.download = fileName;
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
        const contentDisposition = response.headers.get('Content-Disposition');
        let fileName = 'download.mp3';  // Default file name
        if (contentDisposition) {
          const match = contentDisposition.match(/filename="(.+)"/);
          if (match && match[1]) {
            fileName = match[1];
          }
        }
        a.download = fileName;
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
