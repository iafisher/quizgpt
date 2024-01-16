<script setup lang="ts">
import { onMounted, ref } from 'vue';

import * as api from '../api';
import Loading from "@/components/Loading.vue";
import Quiz from "@/components/Quiz.vue";

const props = defineProps(['subjectId']);

const subject = ref<api.Subject|null>(null);
const quizStarted = ref(false);
const quiz = ref<api.Quiz|null>(null);
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  subject.value = await api.getSubject(parseInt(props.subjectId));
  loading.value = false;
});

async function startQuiz() {
  loading.value = true;
  quiz.value = await api.generateQuiz(props.subjectId);
  loading.value = false;
  quizStarted.value = true;
}
</script>

<template>
  <main>
    <!-- TODO: link back to main page -->
    <template v-if="subject">
      <h1>{{ subject.name }}</h1>
      <p class="mb-5">{{ subject.description }}</p>
      <template v-if="!quizStarted">
        <v-btn @click="startQuiz" variant="outlined">Start a new quiz</v-btn>
      </template>
      <template v-else>
        <Quiz :subject="subject" :quiz="quiz" />
      </template>
    </template>
    <Loading :show="loading" />
  </main>
</template>