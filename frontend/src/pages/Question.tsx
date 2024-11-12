import React, { useEffect, useState } from "react";
import SubmissionWidget from "../components/SubmissionWidget";
import { QuestionsPublic, Question, Document } from "../models/questions";
import LeftSideBar from "../components/LeftSideBar";
import Markdown from "react-markdown";

const QuestionPage = () => {
  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(
    null
  );
  const [globalDocs, setGlobalDocs] = useState<Document[]>([]);

  useEffect(() => {
    fetch("/api/questions", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP Error with Status Code: ${response.status}`);
        }
        return response.json();
      })
      .then((responseData: QuestionsPublic) => {
        setQuestions(responseData.questions);
        setGlobalDocs(responseData.global_docs);
        setSelectedQuestion(responseData.questions[0]);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, []);

  // State stores the selected question.
  const handleQuestionClick = (questionNum: number) => {
    const question = questions?.find((q) => q.num - 1 === questionNum) || null;
    setSelectedQuestion(question);
  };

  return (
    <div className="flex">
      <LeftSideBar
        num={questions?.length}
        onTabClick={handleQuestionClick}
      ></LeftSideBar>
      <section className="w-5/6 prose px-3 pt-3">
        {/**<p className="text-2xl">{`Problem ` + selectedQuestion?.num}</p> */}
        <Markdown className="markdown">{"## Problem " + selectedQuestion?.num}</Markdown>
        <Markdown className="markdown">{selectedQuestion?.writeup}</Markdown>
      </section>

      {/** The selected question and the global docs get passed in as props. */}
      {selectedQuestion && (
        <SubmissionWidget question={selectedQuestion} globalDocs={globalDocs} />
      )}
    </div>
  );
};

export default QuestionPage;
