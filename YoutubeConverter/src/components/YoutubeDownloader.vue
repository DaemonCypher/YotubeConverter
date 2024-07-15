<template>
  <div>
    <div class="loader-container" v-if="loading">
      <div id="load">
        <div>G</div>
        <div>N</div>
        <div>I</div>
        <div>D</div>
        <div>A</div>
        <div>O</div>
        <div>L</div>
      </div>
      <h1>Please do not refresh</h1>
    </div>

    <div class="main-content" v-if="!loading">
      <h1>YouTube Downloader</h1>

      <div class="search-container">
        <p>Search YouTube Videos</p>
        <form action="#" class="search-bar" id="search-form" @submit.prevent="getVideoInfo">
          <input type="search" name="search" id="search" placeholder="Enter YouTube URL" v-model="url" pattern="https://www.youtube.com/watch.*" required>
          <button class="search-btn" type="submit">
            <span>Search</span>
          </button>
        </form>
      </div>

      <div v-if="info">
        <br>
        <h2 style="margin-bottom: 20px;">{{ info.title }}</h2>
        <img :src="info.thumbnail_url" alt="Thumbnail"/>
        <br>
        <div class="quality-selection">
          <div class="dropdown-container">
            <div class="container">
              <div class="dropdown" :class="{ active: showVideoDropdown }">
                <div class="select" @click="toggleDropdown('video')">
                  <span>{{ selectedVideoQuality }}</span>
                  <i class="fas fa-chevron-down"></i>
                </div>
                <ul class="dropdown-menu" v-if="showVideoDropdown">
                  <li v-for="quality in videoQualities" :key="quality.id" @click="selectVideoQuality(quality)">
                    {{ quality.name }}
                  </li>
                </ul>
              </div>
            </div>
            <div class="container">
              <div class="dropdown" :class="{ active: showAudioDropdown }">
                <div class="select" @click="toggleDropdown('audio')">
                  <span>{{ selectedAudioQuality }}</span>
                  <i class="fas fa-chevron-down"></i>
                </div>
                <ul class="dropdown-menu" v-if="showAudioDropdown">
                  <li v-for="quality in audioQualities" :key="quality.id" @click="selectAudioQuality(quality)">
                    {{ quality.name }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <button class="action-btn" @click="downloadVideo">Download Video</button>
        <button class="action-btn" @click="downloadAudio">Download Audio</button>
        <button class="action-btn" @click="reset">Convert Next</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      url: '',
      info: null,
      loading: false,
      showVideoDropdown: false,
      showAudioDropdown: false,
      selectedVideoQuality: 'Select Video Quality',
      selectedAudioQuality: 'Select Audio Quality',
      videoQualities: [
        { id: 'best', name: 'Best' },
        { id: '2160', name: '2160p' },
        { id: '1440', name: '1440p' },
        { id: '1080', name: '1080p' },
        { id: '720', name: '720p' },
        { id: '480', name: '480p' },
        { id: '360', name: '360p' },
        { id: '240', name: '240p' },
        { id: '144', name: '144p' }
      ],
      audioQualities: [
        { id: '320', name: 'Exceptional (320 kbps)' },
        { id: '256', name: 'High (256 kbps)' },
        { id: '192', name: 'Medium (192 kbps)' },
        { id: '128', name: 'Low (128 kbps)' }
      ],
      selectedVideoQualityId: '',
      selectedAudioQualityId: ''
    };
  },
  methods: {
    reset() {
      this.url = '';
      this.info = null;
      this.selectedVideoQuality = 'Select Video Quality';
      this.selectedAudioQuality = 'Select Audio Quality';
      this.selectedVideoQualityId = '';
      this.selectedAudioQualityId = '';
      this.showVideoDropdown = false;
      this.showAudioDropdown = false;
    },
    createDownloadLink(blob, defaultFileName) {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = defaultFileName;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    },
    async downloadMedia(endpoint, defaultFileName) {
      try {
        const response = await fetch(`http://localhost:8000/${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            url: this.url,
            quality: endpoint.includes('video') ? this.selectedVideoQualityId : undefined,
            audio_quality: endpoint.includes('audio') ? this.selectedAudioQualityId : undefined
          })
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const blob = await response.blob();
        const contentDisposition = response.headers.get('Content-Disposition');
        let fileName = defaultFileName;
        if (contentDisposition) {
          const match = contentDisposition.match(/filename="(.+)"/);
          if (match && match[1]) {
            fileName = match[1];
          }
        }
        this.createDownloadLink(blob, fileName);
        alert(`${fileName} downloaded successfully`);
      } catch (error) {
        alert(`Error downloading ${defaultFileName}`);
      } finally {
        this.loading = false;
      }
    },
    async downloadVideo() {
      this.loading = true;
      await this.downloadMedia('download_video', 'download.mp4');
    },
    async downloadAudio() {
      this.loading = true;
      await this.downloadMedia('download_audio', 'download.mp3');
    },
    async getVideoInfo() {
      try {
        this.loading = true;
        const response = await fetch(`http://localhost:8000/get_video_info?url=${encodeURIComponent(this.url)}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.info = await response.json();
      } catch (error) {
        console.error('There was a problem with the fetch:', error);
      } finally {
        this.loading = false;
      }
    },
    toggleDropdown(type) {
      if (type === 'video') {
        this.showVideoDropdown = !this.showVideoDropdown;
        this.showAudioDropdown = false;
      } else if (type === 'audio') {
        this.showAudioDropdown = !this.showAudioDropdown;
        this.showVideoDropdown = false;
      }
    },
    selectVideoQuality(quality) {
      this.selectedVideoQuality = quality.name;
      this.selectedVideoQualityId = quality.id;
      this.showVideoDropdown = false;
    },
    selectAudioQuality(quality) {
      this.selectedAudioQuality = quality.name;
      this.selectedAudioQualityId = quality.id;
      this.showAudioDropdown = false;
    }
  }
};
</script>
