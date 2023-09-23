/*
  Warnings:

  - Added the required column `username` to the `Comment` table without a default value. This is not possible if the table is not empty.
  - Added the required column `username` to the `Reply` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Comment" ADD COLUMN     "userImage" TEXT,
ADD COLUMN     "username" TEXT NOT NULL,
ALTER COLUMN "userEmail" DROP NOT NULL;

-- AlterTable
ALTER TABLE "Reply" ADD COLUMN     "userImage" TEXT,
ADD COLUMN     "username" TEXT NOT NULL,
ALTER COLUMN "userEmail" DROP NOT NULL;
