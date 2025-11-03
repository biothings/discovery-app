<script setup>
import { marked } from "marked";

// convert wiki markdown to markdown
function wikiToMarkdown(text) {
  return text.replace(/\[\[([^\]]+)\]\]/g, (match, term) => {
    const cleanTerm = term.trim();
    return `[${cleanTerm}](https://schema.org/${encodeURIComponent(
      cleanTerm
    )})`;
  });
}

// Custom renderer for links
const renderer = {
  link(token) {
    const href = token.href || "#";
    const title = token.title ? ` title="${token.title}"` : "";
    const text = token.text || href;

    return `<a href="${href}"${title} target="_blank" rel="noopener noreferrer">${text}</a>`;
  },
};

// Apply custom renderer
marked.use({ renderer });

const props = defineProps({
  description: {
    type: String,
    default: "No description available",
  },
});
</script>

<template>
  <span v-html="marked.parse(wikiToMarkdown(props.description))"></span>
</template>
