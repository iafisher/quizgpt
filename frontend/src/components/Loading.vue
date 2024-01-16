<script setup lang="ts">
const props = defineProps(["show"]);
</script>

<template>
  <v-overlay :model-value="props.show" class="align-center justify-center">
    <v-progress-circular color="primary" indeterminate size="64"></v-progress-circular>
  </v-overlay>
</template>