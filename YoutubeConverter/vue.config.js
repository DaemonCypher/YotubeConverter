// vue.config.js
module.exports = {
  devServer: {
    allowedHosts: "all", // Allow all hosts to prevent "Invalid Host header" issue
    headers: { "Access-Control-Allow-Origin": "*" }, // Set CORS headers
    historyApiFallback: true,
    compress: true,
    hot: true,
    port: process.env.PORT || 8080, // Use Replit's assigned port
  },
};
