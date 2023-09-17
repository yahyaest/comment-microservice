/*
  Warnings:

  - A unique constraint covering the columns `[userEmail,vote_type,commentId]` on the table `Vote` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[userEmail,vote_type,replyId]` on the table `Vote` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "Vote_userEmail_vote_type_commentId_key" ON "Vote"("userEmail", "vote_type", "commentId");

-- CreateIndex
CREATE UNIQUE INDEX "Vote_userEmail_vote_type_replyId_key" ON "Vote"("userEmail", "vote_type", "replyId");
