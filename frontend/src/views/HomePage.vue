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
    <v-card variant="outlined" href="/create">
      <v-card-title>
        <v-icon icon="mdi-plus"></v-icon>
        Create your own
      </v-card-title>
    </v-card>
  </main>
</template>

<style scoped>
.v-card {
  margin-top: 32px;
}
</style>
