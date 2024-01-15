<script setup lang="ts">
import {ref} from "vue";

import * as api from '../api';
import QuizQuestion from "@/components/QuizQuestion.vue";

const props = defineProps(["quiz", "subject"]);

const empty = [];
for (const _ of props.quiz.questions) {
  empty.push("");
}

const answers = ref(empty.slice());
const comments = ref(empty.slice());
const submitted = ref(false);

async function submitQuiz() {
  // TODO: loading animation while grading quiz
  const gradedQuiz = await api.gradeQuiz(props.subject.name, props.quiz, answers.value);

  for (let i = 0; i < gradedQuiz.results.length; i++) {
    const result = gradedQuiz.results[i];
    comments.value[i] = result.comment;
  }

  submitted.value = true;
}
</script>

<template>
  <div>
    <QuizQuestion v-for="(question, i) in props.quiz.questions" :key="i" v-model="answers[i]" :submitted="submitted"
                  :question="question" :comment="comments[i]"/>
    <v-btn v-if="!submitted" variant="outlined" @click="submitQuiz">Submit</v-btn>
    <!-- TODO: button to generate another quiz after submitted -->
  </div>
</template>