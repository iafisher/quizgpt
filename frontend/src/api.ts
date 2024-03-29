import axios from "axios";

export type IdType = number;

export interface Subject {
    subjectId: IdType;
    name: string;
    description: string;
}

export interface Question {
    text: string;
    rephrase: boolean;
}

// TODO: make port configurable
const BACKEND_URL = "http://localhost:5757";

export async function getSubjectList(): Promise<Subject[]> {
    // TODO: handle API error
    const response = await axios.get(BACKEND_URL + "/subjects/list");
    return response.data.subjects;
}

export async function getSubject(subjectId: IdType): Promise<Subject> {
    // TODO: handle API error
    const response = await axios.get(BACKEND_URL + `/subjects/get/${subjectId}`);
    return response.data;
}

export async function createSubject(name: string, description: string, questions: Question[]): Promise<Subject> {
    // TODO: handle API error
    const response = await axios.post(BACKEND_URL + "/subjects/create", {name, description, questions});
    return response.data.created;
}

const EXAMPLE_QUIZ_QUESTIONS = [
    {
        text: "Give a brief overview of the economy in the 1970s.",
    },
    {
        text: "Name some of the factors that contributed to Nixon's electoral victory in 1968.",
    },
    {
        text: "Who was the Democratic nominee for president in the 1984 election?",
    },
];

export interface Question {
    text: string;
}

export interface Quiz {
    questions: Question[];
}

export async function generateQuiz(subjectId: IdType): Promise<Quiz> {
    // TODO: handle API error
    const response = await axios.post(BACKEND_URL + "/quizzes/generate", {subject_id: subjectId});
    return response.data;
}

const EXAMPLE_COMMENTS = [
    "Correct.",
    "Partially correct. Another factor was the rioting in major cities over the summer of that year.",
    "Incorrect. It was Walter Mondale.",
];

export interface QuestionResult {
    text: string;
    answer: string;
    comment: string;
}

export interface GradedQuiz {
    results: QuestionResult[];
}

export async function gradeQuiz(subject: string, quiz: Quiz, answers: string[]): Promise<GradedQuiz> {
    // TODO: handle API error
    const questions = quiz.questions.map(q => q.text);
    const response = await axios.post(BACKEND_URL + "/quizzes/grade", {subject, questions, answers});
    return response.data;
}