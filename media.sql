/*
 Navicat Premium Data Transfer

 Source Server         : deo
 Source Server Type    : SQLite
 Source Server Version : 3035005 (3.35.5)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005 (3.35.5)
 File Encoding         : 65001

 Date: 20/06/2024 16:21:46
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for media
-- ----------------------------
DROP TABLE IF EXISTS "media";
CREATE TABLE "media" (
  "id" INTEGER,
  "name" TEXT,
  "path" TEXT,
  "views" INTEGER DEFAULT 0,
  "likes" INTEGER DEFAULT 0,
  PRIMARY KEY ("id")
);

PRAGMA foreign_keys = true;
