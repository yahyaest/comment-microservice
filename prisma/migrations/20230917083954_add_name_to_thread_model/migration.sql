/*
  Warnings:

  - Added the required column `name` to the `Thread` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Thread" ADD COLUMN     "name" TEXT NOT NULL;
