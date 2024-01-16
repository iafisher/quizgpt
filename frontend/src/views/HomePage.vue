<script setup lang="ts">
import { onMounted, ref } from 'vue';

import * as api from '../api';
import Loading from "@/components/Loading.vue";

const subjects = ref<api.Subject[]>([]);
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  subjects.value = await api.getSubjectList();
  loading.value = false;
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
    <Loading :show="loading" />
  </main>
</template>

<style scoped>
.v-card {
  margin-top: 32px;
}
</style>
