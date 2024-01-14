<script setup lang="ts">
import { onMounted, ref } from 'vue';

import * as api from '../api';

const subjects = ref<api.Subject[]>([]);

onMounted(async () => {
  subjects.value = await api.getSubjectList();
});
</script>

<template>
  <main>
    <h1>Pick a subject to review.</h1>
    <p class="mb-8">Quizzes generated and graded by OpenAI's GPT models.</p>
    <v-card v-for="subject in subjects" :id="subject.subjectId" :href="'/subject/' + subject.subjectId"
            variant="outlined">
      <v-card-title>{{ subject.name }}</v-card-title>
      <v-card-text>{{ subject.description }}</v-card-text>
    </v-card>
  </main>
</template>
