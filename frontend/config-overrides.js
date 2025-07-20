const { override } = require('customize-cra');

module.exports = {
  webpack: override(
    // You can add Webpack plugins or config tweaks here
  ),

  devServer: (configFunction) => {
    return function (proxy, allowedHost) {
      const config = configFunction(proxy, allowedHost);

      // ✅ This fixes the error
      config.allowedHosts = ['all'];
      config.host = 'localhost';
      config.port = 3000;

      return config;
    };
  }
};
