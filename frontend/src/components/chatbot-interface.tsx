"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  MessageSquare,
  Send,
  Loader2,
  Sparkles,
  Brain,
  Target,
  TrendingUp,
  AlertCircle
} from "lucide-react";
import { reasoningApi, type ReasoningResponse } from "@/lib/api";
import ReactMarkdown from 'react-markdown';
import LiquidEther from '@/components/LiquidEther';

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
    <div className="h-screen flex flex-col bg-background overflow-hidden relative">
      {/* Animated Background */}
      <div className="absolute inset-0 z-0">
        <LiquidEther
          colors={['#6366f1', '#a855f7', '#ec4899']}
          mouseForce={20}
          cursorSize={150}
          isViscous={false}
          viscous={30}
          iterationsViscous={32}
          iterationsPoisson={32}
          resolution={0.5}
          isBounce={false}
          autoDemo={true}
          autoSpeed={0.4}
          autoIntensity={2.0}
          takeoverDuration={0.25}
          autoResumeDelay={3000}
          autoRampDuration={0.6}
        />
      </div>
      
      {/* Content Layer */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full min-h-0 relative z-10">
        {/* Header - Fixed at top */}
        <div className="flex-shrink-0 px-5 sm:px-8 pt-6 sm:pt-8 pb-6 sm:pb-8 border-b border-border/30 bg-background/40 backdrop-blur-2xl">
          <div className="flex items-center gap-3 sm:gap-4">
            <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl bg-accent/10 flex items-center justify-center ring-1 ring-accent/20">
              <Brain className="w-5 h-5 text-accent" />
            </div>
          </div>
        </div>

        {/* Chat Messages - Scrollable Area */}
        <div className="flex-1 overflow-y-auto">
          <div className="px-5 sm:px-8 py-8 sm:py-12 space-y-12 sm:space-y-16">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center py-16 sm:py-20 text-center px-4">
                <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-3xl bg-muted/30 flex items-center justify-center mb-5 sm:mb-6 ring-1 ring-border/30">
                  <MessageSquare className="w-6 h-6 sm:w-7 sm:h-7 text-muted-foreground/50" />
                </div>
                <p className="text-sm text-muted-foreground font-light max-w-md">
                  Ask a question with multiple choice options, and I'll analyze it using advanced reasoning
                </p>
              </div>
            )}
            {messages.map((message) => (
              <div key={message.id} className="space-y-10 sm:space-y-12">
                {message.type === "question" && (
                  <div className="space-y-5 sm:space-y-6">
                    <div className="flex items-start gap-4 sm:gap-5">
                      <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-muted/50 flex items-center justify-center flex-shrink-0 mt-1 ring-1 ring-border/30">
                        <MessageSquare className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-muted-foreground" />
                      </div>
                      <div className="flex-1 space-y-4 sm:space-y-5 min-w-0">
                        <p className="text-sm sm:text-base font-light text-foreground leading-relaxed break-words">
                          {message.question}
                        </p>
                        <div className="grid grid-cols-1 gap-2.5 sm:gap-3">
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
                                className={`text-xs sm:text-sm py-3 sm:py-3.5 px-4 sm:px-5 rounded-xl border break-words transition-all duration-200 ${
                                  isSelected 
                                    ? 'bg-accent/10 border-accent/30 text-accent ring-1 ring-accent/20'
                                    : 'text-muted-foreground bg-card border-border/50 hover:border-border'
                                }`}
                              >
                                <span className="font-medium mr-2 sm:mr-2.5 text-foreground/70">{idx + 1}.</span>
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
                  <div className="flex items-start gap-4 sm:gap-5">
                    <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-accent/10 flex items-center justify-center flex-shrink-0 mt-1 ring-1 ring-accent/20">
                      <Sparkles className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-accent" />
                    </div>
                    <div className="flex-1 space-y-5 sm:space-y-6 min-w-0">
                      <Card className="p-5 sm:p-8 border-border/50 bg-card/50 backdrop-blur-sm shadow-sm">
                        <div className="space-y-6 sm:space-y-8">
                          {/* Answer */}
                          <div>
                            <div className="text-xs font-medium text-muted-foreground mb-2.5 sm:mb-3 uppercase tracking-wider">
                              Selected Answer
                            </div>
                            <div className="text-base sm:text-lg font-light text-foreground break-words leading-relaxed">
                              <span className="text-accent font-medium">{message.result.predicted_answer}.</span> {message.result.answer_text}
                            </div>
                          </div>

                          {/* Metrics */}
                          <div className="grid grid-cols-2 gap-5 sm:gap-6 pt-5 sm:pt-6 border-t border-border/40">
                            <div className="space-y-1.5 sm:space-y-2">
                              <div className="flex items-center gap-1.5 sm:gap-2 text-xs text-muted-foreground font-medium">
                                <TrendingUp className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
                                <span className="uppercase tracking-wider">Confidence</span>
                              </div>
                              <div className="text-2xl sm:text-3xl font-extralight text-foreground tracking-tight">
                                {(message.result.confidence * 100).toFixed(0)}%
                              </div>
                            </div>
                            <div className="space-y-1.5 sm:space-y-2">
                              <div className="flex items-center gap-1.5 sm:gap-2 text-xs text-muted-foreground font-medium">
                                <Target className="w-3 h-3 sm:w-3.5 sm:h-3.5" />
                                <span className="uppercase tracking-wider">Category</span>
                              </div>
                              <div className="text-xs sm:text-sm font-light text-foreground break-words pt-0.5 sm:pt-1">
                                {message.result.category}
                              </div>
                            </div>
                          </div>

                          {/* Reasoning */}
                          <div className="pt-5 sm:pt-6 border-t border-border/40">
                            <div className="text-xs font-medium text-muted-foreground mb-3 sm:mb-4 uppercase tracking-wider">
                              Reasoning
                            </div>
                            <div className="text-xs sm:text-sm leading-relaxed break-words prose prose-sm max-w-none">
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
        <div className="flex-shrink-0 border-t border-border/30 bg-background/50 backdrop-blur-2xl">
          <div className="px-5 sm:px-8 py-6 sm:py-8 space-y-4 sm:space-y-5">
            {error && (
              <div className="flex items-center gap-2.5 sm:gap-3 p-3.5 sm:p-4 rounded-xl bg-destructive/5 border border-destructive/20 ring-1 ring-destructive/10">
                <AlertCircle className="w-4 h-4 text-destructive flex-shrink-0" />
                <p className="text-xs sm:text-sm text-destructive font-light">{error}</p>
              </div>
            )}

            <div className="space-y-4 sm:space-y-5">
              <div>
                <div className="flex items-center justify-between mb-2.5 sm:mb-3">
                  <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
                    Question
                  </label>
                  <span className={`text-xs font-light ${questionLength < 10 ? 'text-muted-foreground/50' : 'text-muted-foreground'}`}>
                    {questionLength}/10
                  </span>
                </div>
                <Input
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="What is the next number: 2, 4, 6, 8, ?"
                  disabled={isProcessing}
                  className="border-border/60 bg-background text-foreground placeholder:text-muted-foreground/50 h-11 text-sm font-light focus-visible:ring-accent/30 rounded-xl"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-muted-foreground mb-2.5 sm:mb-3 block uppercase tracking-wider">
                  Options (exactly 5)
                </label>
                <div className="grid grid-cols-5 gap-1.5 sm:gap-2">
                  {options.map((option, index) => (
                    <Input
                      key={index}
                      value={option}
                      onChange={(e) => handleOptionChange(index, e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder={`${index + 1}`}
                      disabled={isProcessing}
                      className="border-border/60 bg-background text-foreground placeholder:text-muted-foreground/40 h-10 sm:h-11 text-xs sm:text-sm font-light text-center focus-visible:ring-accent/30 rounded-xl"
                    />
                  ))}
                </div>
              </div>

              <Button
                onClick={handleSubmit}
                disabled={isProcessing || !isQuestionValid || options.some(opt => !opt.trim())}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white h-11 sm:h-12 text-sm font-medium disabled:opacity-40 disabled:cursor-not-allowed rounded-xl transition-all duration-200 shadow-lg shadow-purple-500/25 hover:shadow-xl hover:shadow-purple-500/30"
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

