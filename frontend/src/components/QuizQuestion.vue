<script setup lang="ts">
const model = defineModel();

const props = defineProps(["question", "submitted", "comment"]);
</script>

<template>
  <div>
    <!-- TODO: style the text better -->
    <p class="mb-3">{{ props.question.text }}</p>
    <v-textarea v-model="model" variant="outlined" :disabled="submitted"></v-textarea>
    <!-- TODO: style the comment better -->
    <p v-if="submitted && comment">{{ comment }}</p>
  </div>
</template>