/*
  Warnings:

  - You are about to drop the column `vote_type` on the `Vote` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[userEmail,voteType,commentId]` on the table `Vote` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[userEmail,voteType,replyId]` on the table `Vote` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `voteType` to the `Vote` table without a default value. This is not possible if the table is not empty.

*/
-- DropIndex
DROP INDEX "Vote_userEmail_vote_type_commentId_key";

-- DropIndex
DROP INDEX "Vote_userEmail_vote_type_replyId_key";

-- AlterTable
ALTER TABLE "Vote" DROP COLUMN "vote_type",
ADD COLUMN     "username" TEXT,
ADD COLUMN     "voteType" "VoteType" NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "Vote_userEmail_voteType_commentId_key" ON "Vote"("userEmail", "voteType", "commentId");

-- CreateIndex
CREATE UNIQUE INDEX "Vote_userEmail_voteType_replyId_key" ON "Vote"("userEmail", "voteType", "replyId");
