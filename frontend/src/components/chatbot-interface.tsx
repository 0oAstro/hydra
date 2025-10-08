"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Sparkles,
  Send,
  Loader2,
  CheckCircle2,
  Brain,
  Target,
  TrendingUp,
  X
} from "lucide-react";
import { reasoningApi, type ReasoningResponse } from "@/lib/api";
import ReactMarkdown from 'react-markdown';

interface Message {
  id: string;
  type: "question" | "answer";
  question?: string;
  options?: string[];
  result?: ReasoningResponse;
}

export const ChatbotInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [options, setOptions] = useState<string[]>(["", "", "", "", "Another Option"]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string>("");

  const handleOptionChange = (index: number, value: string) => {
    const newOptions = [...options];
    newOptions[index] = value;
    setOptions(newOptions);
  };

  const handleSubmit = async () => {
    if (!question.trim()) {
      setError("Question is required");
      return;
    }
    
    if (question.trim().length < 10) {
      setError("Question must be at least 10 characters");
      return;
    }
    
    if (options.some(opt => !opt.trim())) {
      setError("All 5 options are required");
      return;
    }

    setError("");
    setIsProcessing(true);

    const userMessage: Message = {
      id: `q-${Date.now()}`,
      type: "question",
      question: question.trim(),
      options: options.map(opt => opt.trim()),
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      const result = await reasoningApi.solve({
        question: question.trim(),
        options: options.map(opt => opt.trim()),
      });

      const answerMessage: Message = {
        id: `a-${Date.now()}`,
        type: "answer",
        result,
      };

      setMessages(prev => [...prev, answerMessage]);
      setQuestion("");
      setOptions(["", "", "", "", "Another Option"]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to process");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey && !isProcessing) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const questionLength = question.length;
  const isQuestionValid = questionLength >= 10;

  return (
    <div className="h-screen flex flex-col bg-neutral-950 text-neutral-50">
      <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full min-h-0">
        {/* Header - Fixed at top */}
        <div className="flex-shrink-0 px-4 sm:px-6 pt-6 pb-4 border-b border-neutral-800 bg-neutral-950">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg bg-neutral-100 flex items-center justify-center">
                <Brain className="w-4 h-4 text-neutral-900" />
              </div>
              <div>
                <h1 className="text-lg font-medium tracking-tight text-neutral-50">
                  Reasoning Engine
                </h1>
                <p className="text-xs text-neutral-400">
                  Multi-agent AI reasoning
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Messages - Scrollable Area */}
        <div className="flex-1 overflow-y-auto">
          <div className="px-4 sm:px-6 py-6 pb-8 space-y-6 sm:space-y-8">
            {messages.map((message) => (
              <div key={message.id} className="space-y-6">
                {message.type === "question" && (
                  <div className="space-y-3 sm:space-y-4">
                    <div className="flex items-start gap-3 sm:gap-4">
                      <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-neutral-800 flex items-center justify-center flex-shrink-0 mt-0.5 sm:mt-1">
                        <Sparkles className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-neutral-400" />
                      </div>
                      <div className="flex-1 space-y-2 sm:space-y-3 min-w-0">
                        <p className="text-sm font-medium text-neutral-50 break-words">
                          {message.question}
                        </p>
                        <div className="grid grid-cols-1 gap-1.5 sm:gap-2">
                          {message.options?.map((opt, idx) => {
                            // Find if this option was selected in any answer message
                            const isSelected = messages.some(msg => 
                              msg.type === "answer" && 
                              msg.result && 
                              msg.result.predicted_answer === idx + 1 &&
                              messages.indexOf(msg) > messages.indexOf(message)
                            );
                            
                            return (
                              <div
                                key={idx}
                                className={`text-xs py-2 px-3 rounded-lg border break-words transition-colors ${
                                  isSelected 
                                    ? 'bg-green-950/30 border-green-800 text-green-300'
                                    : 'text-neutral-400 bg-neutral-900 border-neutral-800'
                                }`}
                              >
                                <span className="font-medium mr-2">{idx + 1}.</span>
                                {opt}
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {message.type === "answer" && message.result && (
                  <div className="flex items-start gap-3 sm:gap-4">
                    <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-neutral-100 flex items-center justify-center flex-shrink-0 mt-0.5 sm:mt-1">
                      <CheckCircle2 className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-neutral-900" />
                    </div>
                    <div className="flex-1 space-y-3 sm:space-y-4 min-w-0">
                      <Card className="p-4 sm:p-6 border-neutral-800 bg-neutral-900">
                        <div className="space-y-4 sm:space-y-6">
                          {/* Answer */}
                          <div>
                            <div className="text-xs font-medium text-neutral-400 mb-2 uppercase tracking-wide">
                              Selected Answer
                            </div>
                            <div className="text-base sm:text-lg font-medium text-neutral-50 break-words">
                              {message.result.predicted_answer}. {message.result.answer_text}
                            </div>
                          </div>

                          {/* Metrics */}
                          <div className="grid grid-cols-2 gap-3 sm:gap-4 pt-3 sm:pt-4 border-t border-neutral-800">
                            <div className="space-y-1">
                              <div className="flex items-center gap-1.5 sm:gap-2 text-xs text-neutral-400">
                                <TrendingUp className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
                                <span className="uppercase tracking-wide">Confidence</span>
                              </div>
                              <div className="text-xl sm:text-2xl font-light text-neutral-50">
                                {(message.result.confidence * 100).toFixed(0)}%
                              </div>
                            </div>
                            <div className="space-y-1">
                              <div className="flex items-center gap-1.5 sm:gap-2 text-xs text-neutral-400">
                                <Target className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
                                <span className="uppercase tracking-wide">Category</span>
                              </div>
                              <div className="text-sm font-medium text-neutral-50 break-words">
                                {message.result.category}
                              </div>
                            </div>
                          </div>

                          {/* Reasoning */}
                          <div className="pt-3 sm:pt-4 border-t border-neutral-800">
                            <div className="text-xs font-medium text-neutral-400 mb-2 sm:mb-3 uppercase tracking-wide">
                              Reasoning
                            </div>
                            <div className="text-xs sm:text-sm leading-relaxed text-neutral-300 break-words prose prose-xs sm:prose-sm max-w-none prose-invert">
                              <ReactMarkdown>
                                {message.result.reasoning}
                              </ReactMarkdown>
                            </div>
                          </div>
                        </div>
                      </Card>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Input Area - Fixed at bottom */}
        <div className="flex-shrink-0 border-t border-neutral-800 bg-neutral-900">
          <div className="px-4 sm:px-6 py-4 space-y-3">
            {error && (
              <div className="flex items-center gap-2 p-2.5 rounded-lg bg-red-950/20 border border-red-900/30">
                <X className="w-3.5 h-3.5 text-red-400 flex-shrink-0" />
                <p className="text-xs text-red-400">{error}</p>
              </div>
            )}

            <div className="space-y-3">
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-xs font-medium text-neutral-400 uppercase tracking-wide">
                    Question
                  </label>
                  <span className={`text-xs ${questionLength < 10 ? 'text-neutral-500' : 'text-neutral-400'}`}>
                    {questionLength}/10
                  </span>
                </div>
                <Input
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="What is the next number: 2, 4, 6, 8, ?"
                  disabled={isProcessing}
                  className="border-neutral-800 bg-neutral-950 text-neutral-50 placeholder:text-neutral-500 h-9 text-sm"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-neutral-400 mb-1.5 block uppercase tracking-wide">
                  Options (exactly 5)
                </label>
                <div className="grid grid-cols-5 gap-1.5">
                  {options.map((option, index) => (
                    <Input
                      key={index}
                      value={option}
                      onChange={(e) => handleOptionChange(index, e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder={`${index + 1}`}
                      disabled={isProcessing}
                      className="border-neutral-800 bg-neutral-950 text-neutral-50 placeholder:text-neutral-500 h-9 text-sm text-center"
                    />
                  ))}
                </div>
              </div>

              <Button
                onClick={handleSubmit}
                disabled={isProcessing || !isQuestionValid || options.some(opt => !opt.trim())}
                className="w-full bg-neutral-100 hover:bg-neutral-200 text-neutral-900 h-9 text-sm font-medium disabled:opacity-50"
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Processing
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4 mr-2" />
                    Solve
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

