/*
  Warnings:

  - A unique constraint covering the columns `[createdBy,name]` on the table `Thread` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `createdBy` to the `Thread` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Thread" ADD COLUMN     "createdBy" TEXT NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "Thread_createdBy_name_key" ON "Thread"("createdBy", "name");
