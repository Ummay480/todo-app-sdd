"use client";

import { Check, Trash, Clock } from "lucide-react";
import { Task } from "@/hooks/useTasks";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface TaskCardProps {
  task: Task;
  onToggle: (id: string, completed: boolean) => void;
  onDelete: (id: string) => void;
  isToggling?: boolean;
  isDeleting?: boolean;
}

/**
 * TaskCard component to display individual task information
 * Supports toggling completion status and deletion
 * Reference: @specs/ui/components.md
 */
export function TaskCard({
  task,
  onToggle,
  onDelete,
  isToggling,
  isDeleting,
}: TaskCardProps) {
  const priorityColors = {
    Low: "bg-blue-100 text-blue-800 border-blue-200",
    Medium: "bg-yellow-100 text-yellow-800 border-yellow-200",
    High: "bg-red-100 text-red-800 border-red-200",
  };

  return (
    <div
      className={cn(
        "group flex items-center justify-between p-4 bg-white border rounded-lg shadow-sm transition-all hover:shadow-md",
        task.is_completed ? "bg-gray-50 opacity-75" : "border-gray-200"
      )}
    >
      <div className="flex items-center gap-4 flex-1">
        <button
          onClick={() => onToggle(task.id, !task.is_completed)}
          disabled={isToggling}
          className={cn(
            "flex h-6 w-6 items-center justify-center rounded-full border-2 transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
            task.is_completed
              ? "bg-primary border-primary text-white"
              : "border-gray-300 hover:border-primary"
          )}
          aria-label={task.is_completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {task.is_completed && <Check className="h-4 w-4" />}
        </button>

        <div className="flex flex-col flex-1">
          <h3
            className={cn(
              "text-sm font-medium transition-all",
              task.is_completed ? "text-gray-500 line-through" : "text-gray-900"
            )}
          >
            {task.title}
          </h3>
          {task.description && (
            <p className="text-xs text-gray-500 mt-1 line-clamp-2">
              {task.description}
            </p>
          )}
          <div className="flex items-center gap-3 mt-2">
            <span
              className={cn(
                "text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 rounded-full border",
                priorityColors[task.priority]
              )}
            >
              {task.priority}
            </span>
            <div className="flex items-center gap-1 text-[10px] text-gray-400 font-medium">
              <Clock className="h-3 w-3" />
              <span>{new Date(task.updated_at).toLocaleDateString()}</span>
            </div>
          </div>
        </div>
      </div>

      <button
        onClick={() => onDelete(task.id)}
        disabled={isDeleting}
        className="ml-4 p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
        aria-label="Delete task"
      >
        <Trash className="h-4 w-4" />
      </button>
    </div>
  );
}
