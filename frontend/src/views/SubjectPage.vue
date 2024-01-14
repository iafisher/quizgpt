<script setup lang="ts">
import { onMounted, ref } from 'vue';

import * as api from '../api';
import Quiz from "@/components/Quiz.vue";

const props = defineProps(['subjectId']);

const subject = ref<api.Subject|null>(null);
const quizStarted = ref(false);
const quiz = ref<api.Quiz|null>(null);

onMounted(async () => {
  subject.value = await api.getSubject(parseInt(props.subjectId));
});

async function startQuiz() {
  quiz.value = await api.generateQuiz(props.subjectId);
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
        <Quiz :quiz="quiz" />
      </template>
    </template>
    <template v-else>
      <!-- TODO: loading animation -->
      Loading...
    </template>
  </main>
</template>