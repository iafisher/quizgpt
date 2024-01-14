export type IdType = number;

export interface Subject {
    subjectId: IdType;
    name: string;
    description: string;
}

const EXAMPLE_SUBJECT = {
    subjectId: 1,
    name: "Postwar American history",
    description: "The domestic history of the United States from 1945 to 1990"
};

export async function getSubjectList(): Promise<Subject[]> {
    return [EXAMPLE_SUBJECT];
}

export async function getSubject(subjectId: IdType): Promise<Subject> {
    if (subjectId !== 1) {
        throw "unknown subject ID";
    }

    return EXAMPLE_SUBJECT;
}

export async function createSubject(name: string, description: string, instructions: string): Promise<Subject> {
    return EXAMPLE_SUBJECT;
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

export async function generateQuiz(): Promise<Quiz> {
    return {
        questions: EXAMPLE_QUIZ_QUESTIONS,
    };
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

export async function gradeQuiz(quiz: Quiz, answers: string[]): Promise<GradedQuiz> {
    const results = [];
    for (let i = 0; i < answers.length; i++) {
        results.push({
            text: quiz.questions[i].text,
            answer: answers[i],
            comment: EXAMPLE_COMMENTS[i]
        });
    }

    return { results };
}