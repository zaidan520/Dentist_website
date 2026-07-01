// import { defineConfig } from 'astro/config';
// import tailwind from '@astrojs/tailwind';

// // https://astro.build/config
// export default defineConfig({
//   integrations: [tailwind()]
// });

import { defineConfig } from 'astro/config';
import node from '@astrojs/node';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  output: 'server',
  adapter: node({ mode: 'standalone' }),
  integrations: [tailwind()],
});