import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';
import expressiveCode from 'astro-expressive-code';
import spectre from './package/src';
import { spectreDark } from './src/ec-theme';

// https://astro.build/config
const config = defineConfig({
	site: 'https://aerondight.systems',
	output: 'static',
	integrations: [
		expressiveCode({
			themes: [spectreDark],
		}),
		mdx(),
		sitemap(),
		spectre({
			name: 'Aerondight Systems',
			openGraph: {
				home: {
					title: 'Aerondight Systems',
					description: 'Systematic equity research platform.',
				},
				blog: {
					title: 'Blog',
					description: 'Research and methodology writeups.',
				},
				projects: {
					title: 'Projects',
				},
			},
		}),
	],
});

export default config;
