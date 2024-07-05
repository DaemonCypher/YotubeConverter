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
      reset() {
        this.url = '';
        this.quality = 'best';
        this.audioQuality = '192';
        this.info = null;
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
        const response = await fetch(`http://localhost:8000/${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            url: this.url,
            quality: endpoint.includes('video') ? this.quality : undefined,
            audio_quality: endpoint.includes('audio') ? this.audioQuality : undefined
          })
        });
        if (response.ok) {
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
        } else {
          alert(`Error downloading ${defaultFileName}`);
        }
      },
      async downloadVideo() {
        await this.downloadMedia('download_video', 'download.mp4');
      },
      async downloadAudio() {
        await this.downloadMedia('download_audio', 'download.mp3');
      },
      async getVideoInfo() {
        try {
          const response = await fetch(`http://localhost:8000/get_video_info?url=${encodeURIComponent(this.url)}`);
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