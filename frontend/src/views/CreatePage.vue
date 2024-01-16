<script setup lang="ts">
import {ref} from "vue";
import {useRouter} from "vue-router";

import * as api from "../api";
import Loading from "@/components/Loading.vue";

const form = ref({ name: "", description: "", instructions: "" })
const loading = ref(false);

const router = useRouter();

async function submitForm() {
  // TODO: hook into vuetify's form validation
  if (!form.value.name || !form.value.instructions) {
    return;
  }

  loading.value = true;
  const subject = await api.createSubject(form.value.name, form.value.description, form.value.instructions);
  loading.value = false;
  await router.push({name: "subject", params: {subjectId: subject.subjectId}});
}
</script>

<template>
  <main>
    <!-- TODO: link back to main page -->
    <h1>Create your own quiz</h1>
    <v-form @submit.prevent="submitForm">
      <v-text-field label="Name" v-model="form.name" :rules="[() => !!form.name || 'This field is required.']"></v-text-field>
      <v-textarea label="Description (optional)" v-model="form.description"
                  hint="This will appear on the home page but will not affect the quiz questions the AI model generates."></v-textarea>
      <p class="hint">Give the AI model instructions on what you would like to be quizzed about. You can be specific
        (e.g., 'Ask me what the capital of France is.') or
        general (e.g., 'Ask me general-knowledge questions about the geography of Europe.'). List as many topics or
        themes as you'd like.</p>
      <v-textarea label="Instructions" v-model="form.instructions" :rules="[() => !!form.instructions || 'This field is required.']"></v-textarea>
      <v-btn block type="submit">Submit</v-btn>
    </v-form>
    <Loading :show="loading" />
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
</style>