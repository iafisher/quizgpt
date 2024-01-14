<script setup lang="ts">
import { onMounted, ref } from 'vue';

import * as api from '../api';

const props = defineProps(['subjectId']);

const subject = ref<api.Subject|null>(null);

onMounted(async () => {
  subject.value = await api.getSubject(parseInt(props.subjectId));
});
</script>

<template>
  <main>
    <!-- TODO: link back to main page -->
    <template v-if="subject">
      <h1>{{ subject.name }}</h1>
      <p>{{ subject.description }}</p>
    </template>
    <template v-else>
      <!-- TODO: loading animation -->
      Loading...
    </template>
  </main>
</template>