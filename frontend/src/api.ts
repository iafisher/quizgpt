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