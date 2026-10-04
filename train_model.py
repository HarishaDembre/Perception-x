"""
Training Script for Perception-X Hierarchical Neural Network
Trains on generated dataset to identify:
1. Object vs Illusion (Primary Gating)
2. If Illusion: Which kind of illusion (Geometric, Brightness, Ambiguous)
"""

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from models.neural_net import PerceptionXHierarchicalNet

def train_perception_x(dataset_dir="data/dataset", epochs=12, batch_size=16, lr=0.001):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")

    # Data transforms
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_data = datasets.ImageFolder(os.path.join(dataset_dir, "train"), transform=transform)
    val_data = datasets.ImageFolder(os.path.join(dataset_dir, "val"), transform=transform)

    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False)

    print(f"Dataset classes found: {train_data.classes}")
    # 0_object -> label 0
    # 1_geometric -> label 1
    # 2_brightness -> label 2
    # 3_ambiguous -> label 3

    model = PerceptionXHierarchicalNet(num_illusion_classes=3).to(device)
    criterion_gate = nn.CrossEntropyLoss()
    criterion_illusion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)

    print("\n" + "=" * 70)
    print("  STARTING PERCEPTION-X HIERARCHICAL MODEL TRAINING")
    print("  Task 1: Object vs. Illusion  |  Task 2: Which Kind of Illusion")
    print("=" * 70)

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct_gate = 0
        total_samples = 0

        for images, targets in train_loader:
            images = images.to(device)
            targets = targets.to(device)

            # Target 1: Binary (0 = Object, 1 = Illusion)
            gate_targets = (targets > 0).long()

            optimizer.zero_grad()
            gate_logits, illusion_logits = model(images)

            # Gating loss on all samples
            loss_gate = criterion_gate(gate_logits, gate_targets)

            # Illusion classification loss only on illusion samples
            illusion_mask = targets > 0
            if illusion_mask.sum() > 0:
                # targets 1, 2, 3 -> classes 0, 1, 2
                sub_targets = targets[illusion_mask] - 1
                sub_logits = illusion_logits[illusion_mask]
                loss_illusion = criterion_illusion(sub_logits, sub_targets)
                total_loss = loss_gate + 1.2 * loss_illusion
            else:
                total_loss = loss_gate

            total_loss.backward()
            optimizer.step()

            running_loss += total_loss.item() * images.size(0)
            preds_gate = gate_logits.argmax(dim=1)
            correct_gate += (preds_gate == gate_targets).sum().item()
            total_samples += images.size(0)

        epoch_loss = running_loss / total_samples
        train_gate_acc = correct_gate / total_samples

        # Validation pass
        model.eval()
        val_gate_correct = 0
        val_illusion_correct = 0
        val_illusion_total = 0
        val_total = 0

        with torch.no_grad():
            for images, targets in val_loader:
                images, targets = images.to(device), targets.to(device)
                gate_targets = (targets > 0).long()
                gate_logits, illusion_logits = model(images)

                preds_gate = gate_logits.argmax(dim=1)
                val_gate_correct += (preds_gate == gate_targets).sum().item()
                val_total += targets.size(0)

                # Check illusion accuracy
                illusion_mask = targets > 0
                if illusion_mask.sum() > 0:
                    sub_targets = targets[illusion_mask] - 1
                    sub_preds = illusion_logits[illusion_mask].argmax(dim=1)
                    val_illusion_correct += (sub_preds == sub_targets).sum().item()
                    val_illusion_total += sub_targets.size(0)

        val_gate_acc = val_gate_correct / val_total
        val_ill_acc = (val_illusion_correct / val_illusion_total) if val_illusion_total > 0 else 0.0

        print(f"Epoch [{epoch:02d}/{epochs:02d}] - Loss: {epoch_loss:.4f} | "
              f"Val Object vs Illusion Acc: {val_gate_acc:.1%} | "
              f"Val Illusion Type Acc: {val_ill_acc:.1%}")

    # Save trained model weights
    save_path = "models/perception_x_model.pth"
    torch.save(model.state_dict(), save_path)
    print(f"\nModel training complete! Weights successfully saved to '{save_path}'")
    return save_path

if __name__ == "__main__":
    train_perception_x()
