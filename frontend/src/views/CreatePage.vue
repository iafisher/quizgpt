<script setup lang="ts">
import {ref} from "vue";
import {useRouter} from "vue-router";

import * as api from "../api";
import Loading from "@/components/Loading.vue";

interface Form {
  name: string;
  description: string;
  questions: api.Question[];
}

function blankQuestion() {
  return {text: "", rephrase: true};
}

const form = ref<Form>({name: "", description: "", questions: [blankQuestion()]})
const loading = ref(false);

const router = useRouter();

async function submitForm() {
  // TODO: hook into vuetify's form validation
  if (!form.value.name) {
    return;
  }

  loading.value = true;
  const subject = await api.createSubject(form.value.name, form.value.description, form.value.questions);
  loading.value = false;
  await router.push({name: "subject", params: {subjectId: subject.subjectId}});
}
</script>

<template>
  <main>
    <!-- TODO: link back to main page -->
    <h1>Create your own quiz</h1>
    <v-form @submit.prevent="submitForm">
      <v-text-field label="Name" v-model="form.name"
                    :rules="[() => !!form.name || 'This field is required.']"></v-text-field>
      <v-textarea label="Description (optional)" v-model="form.description"
                  hint="This will appear on the home page but will not affect the quiz questions the AI model generates."></v-textarea>

      <template v-for="(_, i) in form.questions" :key="i">
        <div class="question-input">
          <v-text-field v-model="form.questions[i].text" label="Question"></v-text-field>
          <v-checkbox label="Rephrase?" v-model="form.questions[i].rephrase"></v-checkbox>
          <v-btn @click="form.questions.splice(i, 1)">
            <v-icon icon="mdi-delete"></v-icon>
          </v-btn>
        </div>
      </template>

      <v-btn block @click="form.questions.push(blankQuestion())">Add a question</v-btn>
      <v-btn block type="submit">Submit</v-btn>
    </v-form>
    <Loading :show="loading"/>
  </main>
</template>

<style scoped>
h1 {
  margin-bottom: 16px;
}

.v-text-field {
  margin-bottom: 8px;
}

p.hint {
  margin-bottom: 12px;
}

button {
  margin-top: 16px;
}

.question-input {
  display: flex;
  gap: 10px;
}

.question-input .v-checkbox {
  flex-grow: 0;
}
</style>